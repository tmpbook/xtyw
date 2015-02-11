#coding=utf8
from django import forms
from .models import File, Project, Tag
from django.contrib.auth.models import User, Group

class FileForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['tag'] = forms.ModelChoiceField(
            queryset = Tag.objects.filter(owner=user),
            required = True,
            label = "分类",
            help_text = "不能为空，添加请点",
            error_messages = {'required': "以下是必填项"},
            empty_label = "请至少选择一个",
            widget = forms.Select(
                attrs = {
                    'class': 'form-control',
                    'style': 'width:100%',
                }
            ),
        )
    project = forms.ModelChoiceField(
        queryset = Project.publicProjects.order_by('-add_date'),
        required = False,
        label = "所属项目",
        help_text = "可为空，为了防止混淆，一个文档只能属于一个项目",
        error_messages = {'required': "以下是必填项"},
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'style': 'width:100%',
            }
        ),
    )
    tag = forms.ModelChoiceField(
        queryset = Tag.objects.none(),
    )
    
    group = forms.ModelMultipleChoiceField(
        queryset = Group.objects.order_by('-id'),
        required = True,
        label = "分组",
        help_text = "可以多选",
        error_messages = {'required': "以下至少选择一个"},
        widget = forms.SelectMultiple(
            attrs = {
                'class': 'form-control',
                'style': 'width:100%'
            }
        ),
    )
   
    desc = forms.CharField(
        required = False,
        label = "描述",
        widget = forms.Textarea(
            attrs = {
                'placeholder': u'可以通过描述查找文档',
                'rows': 2,
                'style': 'width:100%',
                'class': 'form-control',
            }
        ),
    )

    file = forms.FileField(
        required = True,
        label = "文档",
        help_text = "大小限制为8G",
        error_messages = {'required': "请选择一个文件"},
    )
   
 
    deleted = forms.BooleanField(
        required = False,
        label = "选中则标记为删除",
        help_text = "默认公开,个人文件不会被项目归类",
        widget = forms.HiddenInput(
            attrs = {
                'style': 'width:100%',
                'class': 'form-control',
            }
        ),
    )

    public = forms.BooleanField(
        required = False,
        label = "公开",
        #help_text = "选中为公开,个人文件不会被项目归类",
    )
    class Meta:
        model = File
        fields = ('project', 'tag', 'group', 'desc', 'file', 'public')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'public', 'added_by', 'desc') 
