from django.test import TestCase

# Create your tests here.
from app01 import models
import pytest
import pymysql


sign = [True]
class TestObj:

    @pytest.mark.parametrize('ret', sign)
    def test_case01(self, ret):
        q = pytest.assume(ret is True)
        if q:
            print(123213132132)
            dbconn = pymysql.connect(host='10.1.25.147',
                                     port=3306,
                                     db='ssm',
                                     user='root',
                                     passwd='12345',
                                     charset="utf8")
            dbcur = dbconn.cursor(cursor=pymysql.cursors.DictCursor)
            sql = "update testcases set api_pass_status='1' where id=9;"
            dbcur.execute(sql)
            dbconn.commit()
            dbcur.close()
            dbconn.close()

        else:
            print(434)
            # models.update_api_pass_status(status='0', id=id)
        # pytest.assume(ret is True)

if __name__ == '__main__':
    # dbconn = pymysql.connect(host='10.1.25.147',
#     #                               port=3306,
#     #                               db='ssm',
#     #                               user='root',
#     #                               passwd='12345',
#     #                               charset="utf8")
#     # from auto_test_platform.settings import DATABASES
#     # #
#     # # dic = DATABASES['default']
#     # # host = dic['HOST']
#     # # port = dic['PORT']
#     # # db = dic['NAME']
#     # # user = dic['USER']
#     # # passwd = dic['PASSWORD']
#     # # charset = "utf8"
#     # # print(host == '10.1.25.147')
#     # # print(port == 3306)
#     # # print(db == 'ssm')
#     # # print(user == 'root')
#     # # print(passwd == 12345)
#     # # print(charset == "utf8")
#     # # dbconn = pymysql.connect(host=dic['HOST'], port=dic['PORT'], db=dic['NAME'], user=dic['USER'], passwd=dic['PASSWORD'], charset="utf8")
#     # dbcur = dbconn.cursor(cursor=pymysql.cursors.DictCursor)
#     # sql = "update testcases set api_pass_status='1' where id=9;"
#     # dbcur.execute(sql)
#     # dbconn.commit()
#     # dbcur.close()
#     # dbconn.close()
    a = """{
	'error': 'Bad Request',
	'errors': [{
		'code': 'Error',
		'field': '',
		'defaultMessage': '账号或密码错误'
	}],
	'status': 400
}"""
    b  = a.replace(r'\'', r'\"')
    print(b)