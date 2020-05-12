from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Document, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ArticleType(Document):
    # 公众号文章类型
    suggest = Completion(analyzer=ik_analyzer)
    w_title = Text(analyzer="ik_max_word")
    w_cover = Keyword()
    w_link = Keyword()
    w_idx = Integer()
    w_create_time = Integer()
    w_update_time = Integer()
    w_read_num = Integer()
    w_watch_num = Integer()
    w_admire_num = Integer()
    w_crawl_time = Integer()
    w_account_id = Integer()

    class Index:
        name = "article"
        doc_type = "link"


class AccountType(Document):
    # 公众号文章类型
    suggest = Completion(analyzer=ik_analyzer)
    a_fakeid = Keyword()
    a_name = Text(analyzer="ik_max_word")
    a_wxid = Keyword()
    a_head_img = Keyword()
    a_intro = Keyword()
    a_type = Keyword()

    class Index:
        name = "account"
        doc_type = "fakeid"


if __name__ == '__main__':
    ArticleType.init()
