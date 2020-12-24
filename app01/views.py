import pytest
import json
from django.shortcuts import render, redirect, HttpResponse, reverse
from app01.myforms import ProjectForm, ApiForm
from app01 import models
from utils.RequestHandler import RequestOp
from jsonpath_rw import parse
from os.path import exists, join
from auto_test_platform.settings import BASE_DIR
# Create your views here.

def add_projects(request):
    form_obj = ProjectForm()
    if request.method == 'POST':
        # 创建一个表单实例，并使用请求中的数据填充它
        form_obj = ProjectForm(request.POST)
        # 检查是否有效
        if form_obj.is_valid():
            dic = form_obj.cleaned_data
            models.insert_project(dic)
            # s = form_obj.cleaned_data['start_time']
            # print(s, type(s))
            return redirect('list_p')
    return render(request, 'add_project.html', {'form_obj':form_obj})

def list_projects(request):
    gene = models.select_all_projects()
    count_testcases = 'count_testcases'
    pass_rate = 'pass_rate'
    return render(request, 'list_projects.html', {'gene': gene, 'count_testcases':count_testcases, 'pass_rate':pass_rate})

def count_testcases(id):
    return models.count_testcases(id)

def pass_rate(id):
    return models.pass_rate(id)


def edit_projects(request, id):
    dic = models.select_one_project(id)
    form_obj = ProjectForm(data=dic)
    if request.method == 'POST':
        form_obj = ProjectForm(request.POST)
        if form_obj.is_valid():
            dic = form_obj.cleaned_data
            models.update_project(id, dic)
            return redirect('list_p')
    return render(request, 'edit_projects.html', {'form_obj':form_obj})

def del_projects(request, id):
    models.del_projects(id)
    return redirect('list_p')

def add_api(request, id):
    proj_dic = models.select_one_project(id)
    form_obj = ApiForm()
    if request.method == 'POST':
        form_obj = ApiForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            models.insert_testcase(id, data)
            return redirect(reverse('list_api', args=(id,)))
    return render(request, 'add_api.html', {'proj_dic':proj_dic, 'form_obj':form_obj})

def list_api(request, id):
    # 这个是projects表的id
    gene = models.slect_testcases_by_projid(id)
    proj_dic = models.select_one_project(id)
    return render(request, 'list_api.html', {'gene':gene, 'proj_dic':proj_dic})

def edit_api(request, id):
    # id是testcases表的id
    testcase = models.select_one_testcase(id)
    proj_id = testcase['proj_id']
    proj_name = models.select_one_project(proj_id)['project_name']
    form_obj = ApiForm(testcase)
    if request.method == 'POST':
        form_obj = ApiForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            print(data)
            models.update_testcase(id, data)
            return redirect(reverse('list_api', args=(proj_id,)))
    return render(request, 'edit_api.html', {'form_obj': form_obj, 'proj_name':proj_name})

def del_api(request, id):
    # id是testcases表的id
    testcase = models.select_one_testcase(id)
    proj_id = testcase['proj_id']
    models.del_testcase(id)
    return redirect(reverse('list_api', args=(proj_id,)))

sign = []
def run_api(request, id):
    # 该id 是testcase的id
    testcase = models.select_one_testcase(id)
    if testcase.get('api_run_status') == '1' and testcase.get('api_run_time') == testcase.get('api_modify_time'):
        return render(request, 'report{}.html'.format(id))

    all_dic_list = list(models.slect_testcases_by_projid(testcase['proj_id']))
    ret = RequestOp(excel_data=testcase, all_excel_data=all_dic_list).get_json()

    # 获取ret的json_path的值
    json_path = testcase.get('json_path')
    exp = parse(json_path)
    DatumInContext_list = exp.find(ret)


    # 获取期望值的json_path的值 得到一个列表
    except_json = json.loads(testcase.get('api_expect'))
    DatumInContext_list2 = exp.find(except_json)

    extracted_list = [i.value for i in DatumInContext_list]
    extracted_list2 = [i.value for i in DatumInContext_list2]

    # ret 与 期望值 用json_path 都获取到值才进行判断
    if extracted_list and extracted_list2:
        ret_extracted_data = extracted_list[0]
        api_except_data = extracted_list2[0]
    else:
        return HttpResponse('json-path 获取字段失败')

    sign.clear()
    sign.append((ret_extracted_data, api_except_data, id))

    report_file_path = join(BASE_DIR, 'templates', 'report{}.html'.format(id))

    # cmd2 = r'pytest views.py::TestObj::test_case01 --html={} --self-contained-html'.format(report_file_path)
    # p = Popen(cmd2, shell=True)
    # p.wait()

    pytest.main(['-s', '-v', __file__, '--html={}'.format(report_file_path), '--self-contained-html'])

    if exists(report_file_path):
        models.update_api_run_time(id)
        models.update_api_run_status(id)
        return render(request, 'report{}.html'.format(id))
    return HttpResponse('生成报告失败')


class TestObj:

    @pytest.mark.parametrize('ret, except_value, id', sign)
    def test_case01(self, ret, except_value, id):
        print(21321312,ret, except_value)
        q = pytest.assume(ret == except_value)
        if q:
            models.update_api_pass_status(status='1', id=id)
        else:
            models.update_api_pass_status(status='0', id=id)

def details_api(request, id):
    return HttpResponse('ok')


if __name__ == '__main__':
    id = 5