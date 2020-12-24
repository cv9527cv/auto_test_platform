import xlrd

class ExcelObj:
    def __init__(self, file_path, index):
        self.sheet_obj = xlrd.open_workbook(file_path).sheet_by_index(index)
        self.temp = []
        self._process_sheet_obj()

    def __repr__(self):
        return '{}'.format(self.temp)

    def _process_sheet_obj(self):
        for line in range(1,self.sheet_obj.nrows):
            self.temp.append(dict(zip(self.sheet_obj.row_values(0), self.sheet_obj.row_values(line))))

    def get_list(self):
        return self.temp


if __name__ == '__main__':
    count = 1
    list_dic = ExcelObj(r'D:\test\untitled2\autotest_platform\static\others\api.xls', 0).get_list()
    for dic in list_dic:
        count += 1
        print(dic)
        if count ==3:
            break





