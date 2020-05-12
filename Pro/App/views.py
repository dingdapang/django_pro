import json
import time
import uuid

# from behave import when
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db.models import Case, When, Q
import math
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.generic.base import View
from elasticsearch import Elasticsearch

from App.es_moudle import ArticleType, AccountType
from App.models import User, Vip_Order, Type, Rank, Account, Article, Follow
from App.views_constant import HTTP_OK, HTTP_USER_EXIST
from App.views_help import send_email_activate, redis_db
from Pro.settings import MEDIA_KEY_PREFIX, ES_HOST


# 登录，注册开始


def home(request):
    '''
    首页
    :param request:
    :return:
    '''
    title = '首页'
    use_id = request.session.get('user_id')

    articles = Article.objects.filter(w_idx=1).order_by('-w_create_time')[0:3]

    if use_id:
        user = User.objects.get(pk=use_id)
        icon = MEDIA_KEY_PREFIX + user.u_icon.url
        username = user.u_username
        return render(request, 'main/home.html', locals())
    else:

        return render(request, 'main/home.html', locals())


def login(request):
    '''
    处理登录
    :param request:
    :return:
    '''
    if request.method == "GET":
        title = 'login'
        return render(request, 'user/login.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = User.objects.filter(u_username=username)

        if users.exists():
            user = users.first()
            if check_password(password, user.u_password):
                if user.is_active:
                    now_time = int(time.time())
                    if user.u_vip_expire_time > now_time:
                        level = user.u_level
                    else:
                        level = 0
                    request.session['user_id'] = user.id
                    request.session['u_level'] = level
                    request.session['type'] = '全部'
                    request.session['screen_time'] = 1
                    request.session['msg'] = ''

                    return redirect(reverse('app:home'))
                else:
                    title = '登录'
                    print('not activate')
                    # request.session['error_message'] = 'not activate'
                    error_message = '！！！not activate'
                    return render(request, 'user/login.html', locals())
            else:

                print('密码错误')
                # request.session['error_message'] = 'password error'
                title = '登录'
                error_message = '！！！password error'
                return render(request, 'user/login.html', locals())
        title = '注册'
        print('用户不存在')
        # request.session['error_message'] = 'user does not exist'
        error_message = ' ！！！user does not exist'
        return render(request, 'user/login.html', locals())


def register(request):
    '''
    处理注册
    :param request:
    :return:
    '''
    if request.method == "GET":
        title = 'register'
        return render(request, 'user/register.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")

        password = make_password(password)

        user = User()
        user.u_username = username
        user.u_email = email
        user.u_password = password
        user.u_icon = icon
        now_time = int(time.time())
        user.u_level = 0
        user.u_vip_expire_time = now_time + 24 * 60 * 60 * 1000
        user.save()

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username, email, u_token)
        # return redirect(reverse('app:home'))
        return render(request, 'user/wait_activate.html', locals())


def activate(request):
    '''
    邮箱激活，为用户分配唯一的UUID
    :param request:
    :return:
    '''
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        cache.delete(u_token)
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        # title = '激活'

        return redirect(reverse('app:home'))


def check_user(request):
    '''
    ajax检查用户名是否被注册
    :param request:
    :return:
    '''
    username = request.GET.get("username")
    user_id = request.session.get('user_id')

    if user_id:
        users = User.objects.filter(~Q(id=user_id)).filter(u_username=username)
    else:
        users = User.objects.filter(u_username=username)

    data = {
        "status": HTTP_OK,
        "msg": 'user can use'
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)


def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    request.session.flush()

    return redirect(reverse('app:home'))


def check_email(request):
    '''
    ajax检查邮箱是否被使用
    :param request:
    :return:
    '''
    email = request.GET.get("email")

    user_id = request.session.get('user_id')

    if user_id:
        users = User.objects.filter(u_email=email).filter(~Q(pk=user_id))
    else:
        users = User.objects.filter(u_email=email)

    data = {
        "status": HTTP_OK,
        "msg": 'user can use'
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)


# 帮助


def help(request):
    '''
    帮助页面
    :param request:
    :return:
    '''
    if request.method == "GET":
        title = '帮助'
        use_id = request.session.get('user_id')
        if use_id:
            user = User.objects.get(pk=use_id)

            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username

            now_time = timezone.now()

        return render(request, 'base_help.html', locals())


# vip部分


def change_vip(request):
    '''
    会员中心页面
    :param request:
    :return:
    '''
    if request.method == "GET":
        title = 'vip'
        use_id = request.session.get('user_id')
        if use_id:
            user = User.objects.get(pk=use_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            u_level = request.session['u_level']
            if int(u_level) == 2:
                level = '高级'
            else:
                level = '初级'
            return render(request, 'vip/vip.html', locals())
        else:
            return redirect(reverse("app:login"))


def order_vip(request):
    # 待做
    '''
    不加入支付宝支付，点击按钮，直接订购成功
    :param request:
    :return:
    '''
    level = request.GET.get('level')
    user_id = request.session.get("user_id")

    orders = Vip_Order.objects.filter(v_status=2).filter(v_user_id=user_id).filter(v_level=level)
    user = User.objects.get(pk=user_id)
    if orders.exists():
        order_obj = orders.first()

        if user.u_level == 2:
            '''
                已有会员，进行续费
            '''
            user.u_vip_expire_time = user.u_vip_expire_time + order_obj.v_expire_time - order_obj.v_start_time
            user.save()
            order_obj.v_status = 1
            order_obj.save()
            data = {
                'status': 200,
                'msg': '订单续费完毕',
                'level': level
            }
        else:
            '''
                    未有会员，进行开通
            '''
            user.u_level = order_obj.v_level
            user.u_vip_expire_time = order_obj.v_expire_time
            user.save()
            order_obj.v_status = 1
            order_obj.save()
            request.session['u_level'] = level

            data = {
                'status': 200,
                'msg': '订单处理完毕',
                'level': level
            }
    else:
        data = {
            'status': 901,
            'msg': '该用户没有未处理的订单',
            'level': level
        }

    return JsonResponse(data=data)


def add_month(request):
    '''
    添加月数，同时修改数据库订单
    :param request:
    :return:
    '''
    level = request.GET.get('level')
    orders = Vip_Order.objects.filter(v_user_id=request.session['user_id']).filter(v_level=level).filter(v_status=2)
    if orders.exists():
        order_obj = orders.first()
        order_obj.v_month = order_obj.v_month + 1
        order_obj.v_expire_time = order_obj.v_expire_time + 30 * 24 * 60 * 60
        order_obj.v_price = order_obj.v_price + 100
    else:
        order_obj = Vip_Order()
        order_obj.v_level = level
        order_obj.v_user_id = request.session['user_id']
        order_obj.v_month = 1
        order_obj.v_start_time = int(time.time())
        order_obj.v_price = 100
        order_obj.v_expire_time = int(time.time()) + 30 * 24 * 60 * 60
    order_obj.save()
    data = {
        'status': 200,
        'msg': 'add_success',
        'level': level,
        'month': order_obj.v_month
    }

    return JsonResponse(data=data)


def sub_month(request):
    '''
    减少月数，同时修改数据库订单
    :param request:
    :return:
    '''
    level = request.GET.get('level')
    orders = Vip_Order.objects.filter(v_user_id=request.session['user_id']).filter(v_level=level).filter(v_status=2)
    if orders.exists():
        order_obj = orders.first()
        if order_obj.v_month > 0:
            order_obj.v_month = order_obj.v_month - 1
            order_obj.v_expire_time = order_obj.v_expire_time - 30 * 24 * 60 * 60
            order_obj.v_price = order_obj.v_price - 100
        else:
            order_obj.v_month = 0
            order_obj.v_expire_time = order_obj.v_expire_time
            order_obj.v_price = 0
        order_obj.save()
        data = {
            'status': 200,
            'msg': 'sub_success',
            'level': level,
            'month': order_obj.v_month
        }
    else:

        data = {
            'status': 200,
            'msg': 'sub_fail',
            'level': level,
            'month': 0
        }

    return JsonResponse(data=data)


# 排行榜


def rank_list(request):
    '''
    排行榜
    :param request:
    :return:
    '''
    title = '排行榜'
    if request.method == "GET":
        use_id = request.session.get('user_id')
        if use_id:
            user = User.objects.get(pk=use_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            u_level = request.session['u_level']
            types = Type.objects.all().order_by('pk')
            if request.session['screen_time'] == 1:
                now_time = int(time.time())
                day_time = now_time - now_time % 86400 + time.timezone
                localtime = time.localtime(time.time())
                r_end_time = day_time - localtime.tm_wday * 24 * 60 * 60
                request.session['screen_time'] = r_end_time
                start_time = '上周'
            else:
                r_end_time = request.session['screen_time']
                end_time = time.strftime("%m月%d日", time.localtime(int(r_end_time)))
                start_timem = time.strftime("%m月%d日", time.localtime(int(r_end_time) - 7 * 24 * 60 * 60))
                if int(time.time()) - int(r_end_time) <= 7 * 24 * 60 * 60:
                    start_time = '上周'
                else:
                    start_time = start_timem + '--' + end_time
            if request.session['type'] == '全部':
                ranks = Rank.objects.filter(r_end_time=r_end_time).order_by("r_index")
                # rank_type = '全部'
            else:
                rank_type = request.session['type']
                ranks = Rank.objects.filter(r_end_time=r_end_time).filter(r_account__a_type=rank_type).order_by(
                    "-r_origin_avg")
            if u_level == 2:
                rans = ranks[0:50]
                count = 50
            else:
                rans = ranks[0:20]
                count = 20

            return render(request, 'rank/list.html', locals())
        else:
            return redirect(reverse("app:login"))


def rank_select(request):
    t_type = request.GET.get("t_type")
    r_end_time = request.session['screen_time']
    u_level = request.session['u_level']
    request.session['type'] = t_type
    ranks = Rank.objects.filter(r_account__a_type=t_type).filter(r_end_time=r_end_time).order_by("-r_origin_avg").all()
    arrs = []
    for rank in ranks:
        rank_l = {}
        rank_l['head_img'] = rank.r_account.a_head_img
        rank_l['name'] = rank.r_account.a_name
        rank_l['is_origin_num'] = rank.r_is_origin_num
        rank_l['put_num'] = rank.r_put_num
        rank_l['all_read_num'] = rank.r_all_read_num
        rank_l['origin_avg'] = rank.r_origin_avg
        rank_l['all_watch_num'] = rank.r_all_watch_num
        rank_l['all_admire_num'] = rank.r_all_admire_num
        rank_l['account_id'] = rank.r_account.id
        arrs.append(rank_l)

    if u_level == 2:
        limit = 50
    else:
        limit = 20

    data = {
        'status': 200,
        'msg': 'success',
        'arrs': arrs,
        'limit': limit
    }
    return JsonResponse(data=data)


def account_detail(request, account_id):
    '''

    :param request:
    :param account_id:公众号id
    :return:
    '''
    if request.method == "GET":
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            account = Account.objects.get(pk=account_id)
            articles = Article.objects.filter(w_account_id=account_id).order_by("-w_create_time", "w_idx")
            follows = Follow.objects.filter(f_user_id=user_id).filter(f_account_id=account_id)
            if follows.exists():

                if follows.first().f_status == 1:
                    follow = 1
                else:
                    follow = -1

            else:
                follow = 0
            print(articles.first().w_create_time)
            return render(request, 'account/account_detail.html', locals())
        else:
            return redirect(reverse("app:login"))


def follow(request):
    '''
    status 1是关注  -1是拉黑
    :param request:
    :return:
    '''

    account_id = request.GET.get("account_id")
    user_id = request.session.get("user_id")

    account = Account.objects.get(pk=account_id)
    user = User.objects.get(pk=user_id)

    follow = Follow()
    follow.f_account = account
    follow.f_user = user
    follow.f_status = 1
    follow.save()

    data = {
        'status': 200,
        'msg': '关注成功',
        'data': [user_id, account_id]
    }
    return JsonResponse(data=data)


def unfollow(request):
    account_id = request.GET.get("account_id")
    user_id = request.session.get("user_id")

    follows = Follow.objects.filter(f_user_id=user_id).filter(f_account_id=account_id).filter(f_status=1)

    if follows.exists():
        follows.delete()
    else:
        pass

    data = {
        'status': 200,
        'msg': '取消关注成功'

    }
    return JsonResponse(data=data)


def block(request):
    account_id = request.GET.get("account_id")
    user_id = request.session.get("user_id")

    account = Account.objects.get(pk=account_id)
    user = User.objects.get(pk=user_id)

    follow = Follow()
    follow.f_account = account
    follow.f_user = user
    follow.f_status = -1
    follow.save()

    data = {
        'status': 200,
        'msg': '拉黑成功',
        'data': [user_id, account_id]
    }
    return JsonResponse(data=data)


def unblock(request):
    account_id = request.GET.get("account_id")
    user_id = request.session.get("user_id")

    follows = Follow.objects.filter(f_user_id=user_id).filter(f_account_id=account_id).filter(f_status=-1)

    if follows.exists():
        follows.delete()
    else:
        pass

    data = {
        'status': 200,
        'msg': '取消拉黑成功'

    }
    return JsonResponse(data=data)


def follow_list(request):
    title = '订阅'
    if request.method == "GET":
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username

            fllow_accounts = Account.objects.filter(follow__f_status=1).filter(follow__f_user_id=user_id)

            block_accounts = Account.objects.filter(follow__f_status=-1).filter(follow__f_user_id=user_id)

            return render(request, 'follow/follow.html', locals())
        else:
            return redirect(reverse("app:login"))


def time_select(request):
    screen_time = request.GET.get("screen_time")
    request.session['screen_time'] = screen_time
    type = request.session['type']

    data = {
        'status': 200,
        'msg': "success",
        'type': type
    }
    return JsonResponse(data=data)


# 搜索建议
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        article_datas = []
        account_datas = []

        if key_words:
            s = ArticleType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 5
            })
            suggestions = s.execute()
            for match in suggestions.suggest.my_suggest[0].options:
                source = match._source
                article_datas.append(source["w_title"])
            # print(re_datas)
            k = AccountType.search()
            k = k.suggest('my_suggest', key_words, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 5
            })
            suggestions = k.execute()
            for match in suggestions.suggest.my_suggest[0].options:
                source = match._source
                account_datas.append(source["a_name"])
            print(account_datas)


            data = {
                'status': 200,
                'msg': 'success',
                'article_datas': article_datas,
                'account_datas': account_datas
            }
        return JsonResponse(data=data, safe=False)


def search(request):
    '''
        公众号搜索
    :param request:
    :return:
    '''
    client = Elasticsearch(hosts=[ES_HOST])
    title = 'search'
    index_name = 'account'
    if request.method == "GET":
        redis_server = redis_db()
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            keyword = request.GET.get('keyword')
            page = request.GET.get('page')
            search_type = request.GET.get('search_type')
            if search_type == 'title':
                pass
            else:

                # hot_searchs = redis_server.get_search_rank(0, 5)
                if page:
                    page = page
                else:
                    page = 1
                if keyword:

                    redis_server.save_search(keyword)
                    if keyword != request.session['keyword']:
                        page = 1
                        request.session['keyword'] = keyword
                    else:
                        page = page

                    old_accounts = Account.objects.filter(a_name__contains=keyword)

                    response = client.search(
                        index=index_name,
                        body={
                            "query": {
                                "multi_match": {
                                    "query": keyword,
                                    "fields": ["a_name"]
                                }
                            },
                            "from": 0,
                            "size": 10,
                            "highlight": {
                                "pre_tags": ['<span class="keyWord">'],
                                "post_tags": ['</span>'],
                                "fields": {
                                    "title": {},
                                    "content": {},
                                }
                            }
                        }
                    )
                    hits = response.get("hits").get('hits')
                    # print(hits)

                    hit_list = []
                    for hit in hits:
                        from collections import defaultdict
                        hit_dict = defaultdict(str)
                        if "highlight" not in hit:
                            hit["highlight"] = {}
                        if "a_name" in hit["highlight"]:
                            hit_dict["a_name"] = "".join(hit["highlight"]["a_name"])
                        else:
                            hit_dict["a_name"] = hit["_source"]["a_name"]
                        hit_dict["a_head_img"] = hit["_source"]["a_head_img"]
                        if 'a_intro' in hit["_source"]:
                            hit_dict["a_intro"] = hit["_source"]["a_intro"]
                        else:
                            hit_dict["a_intro"] = ''

                        hit_dict["a_fakeid"] = hit["_source"]["a_fakeid"]
                        hit_dict["account_id"] = hit["_source"]["account_id"]

                        hit_list.append(hit_dict)

                    old_accounts = hit_list
                    account_len = len(old_accounts)
                    page_count = math.ceil(account_len / 5)
                    accounts = old_accounts[(int(page) - 1) * 5:int(page) * 5]
                    hot_searchs = redis_server.get_search_rank(0, 5)
                    return render(request, 'search/search.html', locals())
                else:
                    request.session['keyword'] = ''
                    keyword = ''
                    hot_searchs = redis_server.get_search_rank(0, 5)
                    return render(request, 'search/search.html', locals())
        else:
            return redirect(reverse("app:login"))


def person(request):
    title = '个人中心'
    if request.method == "GET":
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            msg = request.session['msg']

            request.session['msg'] = ''
            return render(request, 'main/person.html', locals())
        else:
            return redirect(reverse("app:login"))
    elif request.method == "POST":
        act = 1
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")
        password = make_password(password)
        user.u_username = username
        user.u_email = email
        user.u_password = password
        user.u_icon = icon
        user.is_active = 0

        user.save()

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username, email, u_token)

        request.session['msg'] = "修改信息成功"
        return render(request, 'user/wait_activate.html', locals())


def ali_pay(request):
    '''
    支付宝支付，后面再做
    :param request:
    :return:
    '''
    return None

# def alipay(request):
#
#     # 构建支付客户端，AlipayClient
#     alipay_client = AliPay(
#         appid=ALIPAY_APPID,
#         app_notify_url=None,  # 默认回调url
#         app_private_key_string=APP_PRIVATE_KEY_STRING,
#         # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         alipay_public_key_string=ALIPAY_PUBLIC_KEY_STRING,
#         sign_type="RSA",  # RSA 或者 RSA2
#         debug=False  # 默认False
#     )
#     # 使用Alipay进行支付请求的发起
#
#     subject = "蓝牙耳机"
#
#     # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
#     order_string = alipay_client.api_alipay_trade_page_pay(
#         out_trade_no="110",
#         total_amount=100,
#         subject=subject,
#         return_url="https://www.1000phone.com",
#         notify_url="https://www.1000phone.com"  # 可选, 不填则使用默认notify url
#     )
#
#     # 客户端操作
#     return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

# def owner_page(request, obj):
#     """
#     # 自定义分页器
#     :param request: request请求
#     :param obj: 分页对象
#     :return: 所在页码的对象集，所有页码，当前页码，分页对象的总数
#     """
#     current_page = 1
#     all_page = 1
#     page_type = ''
#     PAGE_SIZE = 5
#     try:
#         current_page = int(request.GET.get('cur', '1'))
#         all_page = int(request.GET.get('all', '1'))
#         page_type = str(request.GET.get('action', ''))  # 向前翻页还是向下翻页
#     except ValueError:
#         current_page = 1
#         all_page = 1
#         page_type = ''
#
#     if page_type == 'next':
#         current_page += 1
#     elif page_type == 'previous':
#         current_page -= 1
#     if isinstance(obj, list):
#         count = len(obj)
#     else:
#         count = obj.count()
#     start = (current_page - 1) * PAGE_SIZE
#     end = current_page * PAGE_SIZE
#     data = obj[start:end]
#
#     if current_page == 1 and current_page == 1:  # 标记1
#         all_page = math.ceil(count / PAGE_SIZE)
#     return data, all_page, current_page, count


def search_article(request):
    client = Elasticsearch(hosts=["127.0.0.1"])
    title = 'search'
    index_name = 'article'
    if request.method == "GET":
        redis_server = redis_db()
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            icon = MEDIA_KEY_PREFIX + user.u_icon.url
            username = user.u_username
            keyword = request.GET.get('keyword')
            page = request.GET.get('page')
            if page:
                page = int(page)
                # print(page)
            else:
                page = 1
            search_type = request.GET.get('search_type')
            if search_type == 'title':
                response = client.search(
                    index=index_name,
                    body={
                        "query": {
                            "multi_match": {
                                "query": keyword,
                                "fields": ["w_title"]
                            }
                        },
                        "from": (page - 1) * 10,
                        "size": 10,
                        "highlight": {
                            "pre_tags": ['<span class="keyWord">'],
                            "post_tags": ['</span>'],
                            "fields": {
                                "title": {},
                                "content": {},
                            }
                        }
                    }
                )

                # res = json.dumps(response)
                redis_server.save_search(keyword)

                total = response.get("hits").get('total')
                hits = response.get("hits").get('hits')
                hit_list = []
                for hit in hits:
                    from collections import defaultdict
                    hit_dict = defaultdict(str)
                    if "highlight" not in hit:
                        hit["highlight"] = {}
                    if "w_title" in hit["highlight"]:
                        hit_dict["w_title"] = "".join(hit["highlight"]["w_title"])
                    else:
                        hit_dict["w_title"] = hit["_source"]["w_title"]
                    hit_dict["w_cover"] = hit["_source"]["w_cover"]
                    hit_dict["w_link"] = hit["_source"]["w_link"]
                    hit_dict["w_read_num"] = hit["_source"]["w_read_num"]
                    hit_dict["w_watch_num"] = hit["_source"]["w_watch_num"]
                    hit_dict["w_admire_num"] = hit["_source"]["w_admire_num"]

                    hit_list.append(hit_dict)

                all_hits = hit_list
                hot_searchs = redis_server.get_search_rank(0, 5)
                return render(request, 'search/search.html', locals())
        else:
            return redirect(reverse("app:login"))