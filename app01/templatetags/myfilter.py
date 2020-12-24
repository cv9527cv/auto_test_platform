from django import template
import sys
register = template.Library()

@register.filter(name='fu')
def fu(arg, id):
    method = getattr(sys.modules['app01.views'], arg)
    return method(id)

"""

select (concat(round((select count(id) from testcases where proj_id=6  and api_pass_status='1')/(select count(id) from testcases where proj_id=6)*100,1), '%')) as 'pass_rate';

"""

if __name__ == '__main__':
    sql = "select (concat(round((select count(id) from testcases where proj_id={}  and api_pass_status='1')/(select count(id) from testcases where proj_id={})*100,1), '%')) as 'pass_rate';".format(6, 9)

    sql = "select (concat(round((select count(id) from testcases where proj_id=%s  and api_pass_status='1')/(select count(id) from testcases where proj_id=%s)*100,1), '%%')) as 'pass_rate';" %(1, 1)
    print(sql)