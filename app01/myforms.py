from django import forms

class ProjectForm(forms.Form):
    project_name = forms.CharField(max_length=100, label='项目名称')
    comment = forms.CharField(widget=forms.Textarea, label='项目描述', required=False)
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'date'}), label='开始时间')
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'date'}), label='结束时间')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ApiForm(forms.Form):
    api_name = forms.CharField(label='接口名称', max_length=100)
    api_desc = forms.CharField(label='接口描述', widget=forms.Textarea)
    api_url = forms.CharField(label='接口地址', max_length=100)
    req_method = (
        ('0', 'get'),
        ('1', 'post'),
        ('2', 'put'),
        ('3', 'delete')
    )
    api_method = forms.ChoiceField(label='请求类型', choices=req_method)
    api_header = forms.CharField(label='请求头')
    api_para = forms.CharField(label='请求参数', required=False)
    api_body = forms.CharField(label='请求体参数')
    api_expect = forms.CharField(label='预期结果')
    json_path = forms.CharField(label='断言位置')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})