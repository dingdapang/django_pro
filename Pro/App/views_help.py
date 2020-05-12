import redis
from django.core.mail import send_mail
from django.template import loader

from Pro.settings import EMAIL_HOST_USER, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY


def send_email_activate(username, receive, u_token):

    subject = '%s  Activate' % username

    from_email = EMAIL_HOST_USER

    recipient_list = [receive, ]

    data = {
        'username': username,
        'activate_url': 'http://dinglibo.top/app/activate/?u_token={}'.format(u_token)
    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message="", html_message=html_message, from_email=from_email, recipient_list=recipient_list)


class redis_db():
    def __init__(self):
        pool = redis.ConnectionPool(decode_responses=True, encoding='utf-8', host=REDIS_HOST, port=REDIS_PORT,
                                                                 password=REDIS_PASSWORD, db=REDIS_DB)
        self.server = redis.Redis(connection_pool=pool)

    def save_search(self, keyword):

        if not self.server.zscore(REDIS_KEY, keyword):  # 查询分数
            self.server.zadd(REDIS_KEY, {keyword: 1})
        else:
            self.server.zincrby(REDIS_KEY, 1, keyword)  # 增加分数

    def close(self):
        self.server.close()

    def get_search_rank(self, start, end):
        # name，redis的name
        # start，有序集合索引起始位置（非分数）
        # end，有序集合索引结束位置（非分数）
        # desc，排序规则，默认按照分数从小到大排序
        # withscores，是否获取元素的分数，默认只获取元素的值
        # score_cast_func，对分数进行数据转换的函数
        key = self.server.zrange(REDIS_KEY, start, end, desc=True, withscores=False, score_cast_func=float)
        return key


if __name__ == '__main__':
    db = redis_db()
    # db.save_search('hehe')
    key = db.get_search_rank(0, 5)
    print(key)