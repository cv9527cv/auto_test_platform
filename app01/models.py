from django.db import models
import pymysql
import datetime
from auto_test_platform.settings import DATABASES


dic = DATABASES['default']
# Create your models here.
class DB(object):

    def __init__(self, host=dic['HOST'], port=dic['PORT'], db=dic['NAME'], user=dic['USER'], passwd=dic['PASSWORD'], charset="utf8"):
        # 创建数据库连接
        self.dbconn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)

        # 创建字典型游标(返回的数据是字典类型)
        self.dbcur = self.dbconn.cursor(cursor=pymysql.cursors.DictCursor)

    # __enter__() 和 __exit__() 是with关键字调用的必须方法
    # with本质上就是调用对象的enter和exit方法
    def __enter__(self):
        # 返回游标
        return self.dbcur

    def __exit__(self, exc_type, exc_value, exc_trace):
        # 提交事务
        self.dbconn.commit()

        # 关闭游标
        self.dbcur.close()

        # 关闭数据库连接
        self.dbconn.close()


def insert_project(data):
    project_name = data['project_name']
    comment = data['comment']
    start_time = data['start_time'].strftime('%Y-%m-%d')
    end_time = data['end_time'].strftime('%Y-%m-%d')
    sql = 'insert into projects(project_name, comment, start_time, end_time) values(%s, %s, %s, %s);'
    with DB() as dbcur:
        dbcur.execute(sql, (project_name, comment, start_time, end_time))

def insert_testcase(id, data):
    api_name = data['api_name']
    api_desc = data['api_desc']
    api_url = data['api_url']
    api_method = data['api_method']
    api_para = data['api_para']
    api_body = data['api_body']
    api_expect = data['api_expect']
    api_header = data['api_header']
    json_path = data['json_path']
    sql = 'insert into testcases(api_name, api_desc, api_url, api_method, api_header, api_para, api_body, api_expect, proj_id, json_path) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    with DB() as dbcur:
        dbcur.execute(sql, (api_name, api_desc, api_url, api_method, api_header, api_para, api_body, api_expect, id, json_path))

def select_all_projects():
    sql = 'select * from projects;'
    with DB() as dbcur:
        count = dbcur.execute(sql)
        for i in range(count):
            yield dbcur.fetchone()

def select_one_project(id):
    sql = 'select * from projects where id = %s;'
    with DB() as dbcur:
        dbcur.execute(sql, id)
        ret = dbcur.fetchone()
    return ret

def slect_testcases_by_projid(id):
    sql = 'select * from testcases where proj_id=%s;'
    with DB() as dbcur:
        count = dbcur.execute(sql, id)
        for i in range(count):
            yield dbcur.fetchone()

def select_one_testcase(id):
    sql = 'select * from testcases where id = %s;'
    with DB() as dbcur:
        dbcur.execute(sql, id)
        ret = dbcur.fetchone()
    return ret

def update_project(id, data):
    sql = 'update projects set project_name=%s,comment=%s,start_time=%s,end_time=%s where id=%s;'
    project_name = data['project_name']
    comment = data['comment']
    start_time = data['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    end_time = data['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    with DB() as dbcur:
        dbcur.execute(sql, (project_name, comment, start_time, end_time, id))

def update_testcase(id, data):
    sql = 'update testcases set api_name=%s, api_desc=%s, api_url=%s, api_method=%s, api_header=%s, api_para=%s, api_body=%s, api_expect=%s, json_path=%s where id=%s;'
    api_name = data['api_name']
    api_desc = data['api_desc']
    api_url = data['api_url']
    api_method = data['api_method']
    api_para = data['api_para']
    api_body = data['api_body']
    api_expect = data['api_expect']
    api_header = data['api_header']
    json_path = data['json_path']
    with DB() as dbcur:
        dbcur.execute(sql, (api_name, api_desc, api_url, api_method, api_header, api_para, api_body, api_expect, id, json_path))

def del_projects(id):
    sql = 'delete from projects where id=%s;'
    with DB() as dbcur:
        dbcur.execute(sql, id)

def del_testcase(id):
    sql = 'delete from testcases where id=%s;'
    with DB() as dbcur:
        dbcur.execute(sql, id)

def update_api_run_time(id):
    sql = 'update testcases set api_run_time=now() where id=%s;'
    with DB() as dbcur:
        dbcur.execute(sql, id)

def update_api_run_status(id):
    sql = "update testcases set api_run_status='1' where id=%s;"
    with DB() as dbcur:
        dbcur.execute(sql, id)

def update_api_pass_status(status, id):
    sql = "update testcases set api_pass_status=%s where id=%s;"
    with DB() as dbcur:
        dbcur.execute(sql, (status, id))

def count_testcases(id):
    sql = "select count(id) from testcases where proj_id=%s;"
    with DB() as dbcur:
        dbcur.execute(sql, id)
        a = dbcur.fetchone().get('count(id)')
        return a

def pass_rate(id):
    sql = "select (concat(round((select count(id) from testcases where proj_id=%s  and api_pass_status='1')/(select count(id) from testcases where proj_id=%s)*100,1), '%%')) as 'pass_rate';"
    with DB() as dbcur:
        dbcur.execute(sql, (id, id))
        a = dbcur.fetchone().get('pass_rate')
        return a


if __name__ == '__main__':
    # update_api_run_time(9)
    # update_api_run_status(9)
    # update_api_pass_status(status='1', id=9)
    a = count_testcases(6)
    print(a)