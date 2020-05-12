import datetime

from django import template
register = template.Library()


@register.filter(name='print_timestamp')
def print_timestamp(timestamp):
    '''
    时间戳转年月日
    :param timestamp: 时间戳
    :return: 年-月-日 时:分:秒
    '''
    # # specify format here
    # return time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime(timestamp))
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


register.filter(print_timestamp)

# print(print_timestamp(1588891847))