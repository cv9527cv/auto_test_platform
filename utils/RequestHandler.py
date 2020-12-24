import requests
import json
import re
from jsonpath_rw import parse
from utils.Excelhandler import ExcelObj

token_dic = {}

class RequestOp:
    def __init__(self, excel_data, all_excel_data):
        self.excel_data = excel_data
        self.all_excel_data = all_excel_data
        self.ret = self._send_msg()

        # MySQL数据来源不需要保存数据，不用执行_save_msg方法，excel的就需要
        # self._save_msg(self.ret)

    def _send_msg(self):
        # excel文件用以下关键字取值。
        #         # a=self._check(self.excel_data['url'])
        #         # c=json.loads(self._check(self.excel_data['header']))
        #         # d=self._check(self.excel_data['body_data']).encode('utf-8')

        # 数据库用以下关键字取值 ------------------------。
        req_method_dic = {'0': 'get', '1': 'post', '2': 'put', '3': 'delete'}

        a=self._check(self.excel_data['api_url'])
        c=json.loads(self._check(self.excel_data['api_header']))
        d=self._check(self.excel_data['api_body']).encode('utf-8')
        e = req_method_dic[self.excel_data['api_method']]
        f = json.loads(self.excel_data['api_para'])
        # f = self.excel_data['api_para']
        # print(f, type(f))



        # --------------------------------------------
        ret2 = [
            a, c, d, e, f
        ]
        print('ret2:', ret2)

        ret = requests.request(
            url=a,
            method=e,
            headers=c,
            params=f,
            data=d,
        )
        return ret

    # 用于excel的数据提取字段值
    def _check2(self, stri):

        """
        :param stri: 解析的字段，比如  {"Authorization": "$login>response_json>data$"}
        :return: 解析完成的字段        {"Authorization": "Bear Jyrfcvybubniundefe"}
        """
        # 正则提取表达式
        pattern = re.compile('\$(.*?)\$')
        extracted_content = pattern.findall(stri)
        if extracted_content:
            for content in extracted_content:
                # content.strip('$')
                id, title, json_path = content.split('>')
                # 获取目标字段，并替换正则
                for dic in self.all_excel_data:
                    if dic['api_name'] == id:

                        # 用jsonpath-rw的parse方法，获取json的某一个字段值
                        exp = parse(json_path)
                        extracted_list = [i.value for i in exp.find(dic[title])]
                        extracted_data = extracted_list[0]
                        if not isinstance(extracted_data, str):
                            extracted_data = str(extracted_data)

                        # 替换
                        if id == 'login':
                            extracted_data = 'Bearer ' + extracted_data
                            stri = pattern.sub(extracted_data, stri)
                            return stri
                        stri = pattern.sub(extracted_data, stri)
        return stri

    # 用于MySQL 数据提取字段值
    def _check(self, stri):

        """
        :param stri: 解析的字段，比如  {"Authorization": "$login>data$"}
        :return: 解析完成的字段        {"Authorization": "Bear Jyrfcvybubniundefe"}
        """
        # 正则提取表达式
        pattern = re.compile('\$(.*?)\$')
        extracted_content = pattern.findall(stri)
        if extracted_content:
            for content in extracted_content:
                # content.strip('$')
                api_name, json_path = content.split('>')
                # 获取目标字段，并替换正则
                for dic in self.all_excel_data:
                    if dic['api_name'] == api_name:

                        # 获取依赖的response_json
                        response_json = RequestOp(excel_data=dic, all_excel_data=self.all_excel_data).get_json()
                        # 用jsonpath-rw的parse方法，获取json的某一个字段值
                        exp = parse(json_path)
                        extracted_list = [i.value for i in exp.find(response_json)]
                        extracted_data = extracted_list[0]
                        if not isinstance(extracted_data, str):
                            extracted_data = str(extracted_data)

                        # 替换
                        if api_name == 'login':
                            # 特殊情况，依赖是token时，需要加上‘Bearer ’
                            extracted_data = 'Bearer ' + extracted_data
                            stri = pattern.sub(extracted_data, stri)
                            return stri
                        # 一般情况，直接替换即可
                        stri = pattern.sub(extracted_data, stri)
        return stri


    def _save_msg(self, data):
        # data 是url请求返回的response对象
        # isinstance(ret, requests.Response)
        json_content = data.json()
        if json_content:
            # if self.excel_data['id'] == 'login_1':
            #     self.excel_data['response_json'] = json_content
            self.excel_data['response_json'] = json_content


    def get_json(self):
        if self.ret.json():
            return self.ret.json()


if __name__ == '__main__':
    count = 1
    list_dic = ExcelObj(r'D:\test\auto_test_platform\static\others\api.xlsx', 0).get_list()
    for dic in list_dic:
        ret = RequestOp(dic, list_dic).get_json()

        print('ret:', ret)
        count += 1
        if count == 6:
            for i in list_dic:
                print(21212, i)
            break
