import time

from django.db import models
from django.utils import timezone


class User(models.Model):
    '''
    用户
    '''
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icons/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    u_level = models.IntegerField(default=0)
    u_vip_expire_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'wa_user'


class Vip_Order(models.Model):
    '''
    vip订单
    '''
    v_user = models.ForeignKey(User, on_delete=models.CASCADE)
    v_level = models.IntegerField(default=0)
    v_month = models.IntegerField(default=0)
    v_price = models.IntegerField(default=0)
    v_start_time = models.IntegerField(default=0)
    v_expire_time = models.IntegerField(default=0)
    last_change_time = models.DateTimeField(auto_now=True)
    v_status = models.IntegerField(default=2)

    class Meta:
        db_table = 'wa_vip_order'


class Account(models.Model):
    '''
    公众号列表
    '''
    a_fakeid = models.CharField(max_length=32, unique=True)
    a_name = models.CharField(max_length=50)
    a_wxid = models.CharField(max_length=32)
    a_head_img = models.CharField(max_length=255)
    a_intro = models.CharField(max_length=255,null=True)
    a_type = models.CharField(max_length=10)
    a_update_time = models.IntegerField(default=0)
    a_change_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wa_account'


class Type(models.Model):
    '''
    公众号类型表
    '''
    t_type = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'wa_type'


class Article(models.Model):
    '''
    公众号文章阅读点赞表
    '''
    w_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    w_title = models.CharField(max_length=64)
    w_cover = models.CharField(max_length=255)
    w_link = models.CharField(max_length=255, unique=True)
    w_idx = models.IntegerField(default=0)
    w_create_time = models.IntegerField(default=0)
    w_update_time = models.IntegerField(default=0)
    w_read_num = models.IntegerField(default=0)
    w_watch_num = models.IntegerField(default=0)
    w_admire_num = models.IntegerField(default=0)
    w_crawl_time = models.IntegerField(default=0)
    w_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'wa_article'


class Rank(models.Model):
    '''
    榜单的统计数据
    '''
    r_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    r_is_origin_num = models.IntegerField(default=0)
    r_put_num = models.IntegerField(default=0)
    r_all_read_num = models.IntegerField(default=0)
    r_origin_avg = models.IntegerField(default=0)
    r_all_watch_num = models.IntegerField(default=0)
    r_all_admire_num = models.IntegerField(default=0)
    r_index = models.IntegerField(default=0)
    r_start_time = models.IntegerField(default=0)
    r_end_time = models.IntegerField(default=0)
    r_update_time = models.IntegerField(default=0)

    class Meta:
        db_table = 'wa_rank'


class Follow(models.Model):
    '''
    用户关注，拉黑公众号列表
    '''
    f_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    f_user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'wa_follow'






