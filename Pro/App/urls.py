from django.urls import path

from App import views
from App.views import SearchSuggest

urlpatterns = [

    # path('test/', views.test, name='test'),

    path('home/', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('activate/', views.activate, name='activate'),
    path('checkuser/', views.check_user, name='checkuser'),
    path('checkemail/', views.check_email, name='checkemail'),
    path('logout/', views.logout, name='logout'),

    path('person/', views.person, name='person'),




    # 榜单
    path('ranklist/', views.rank_list, name='rank_list'),
    path('rankselect/', views.rank_select, name='rank_select'),
    path('timeselect/', views.time_select, name='time_select'),



    # 公众号详情
    path('accountdetail/<int:account_id>/', views.account_detail, name='account_detail'),




    # 搜索
    path('search/', views.search, name='search'),
    path('searcharticle/', views.search_article, name='search_article'),
    path('searchsuggest/', SearchSuggest.as_view(), name='suggest'),



    # 订阅

    path('followlist/', views.follow_list, name='follow_list'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('block/', views.block, name='block'),
    path('unblock/', views.unblock, name='unblock'),





    # 会员中心
    path('vip/', views.change_vip, name='vip'),
    path('addmonth/', views.add_month, name='add_month'),
    path('submonth/', views.sub_month, name='sub_month'),
    path('ordervip/', views.order_vip, name='ordervip'),
    path('alipay/', views.ali_pay, name='alipay'),


    # 帮助
    path('help/', views.help, name='help'),




]