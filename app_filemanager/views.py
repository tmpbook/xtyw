#coding=utf-8
# vim: ai ts=4 sts=4 et sw=4
import datetime
# ----------------------
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404, HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views import generic
from .models import File, Project
from django.contrib.auth.models import User
from .forms import FileForm, ProjectForm
from django.utils import timezone
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.servers.basehttp import FileWrapper
import mimetypes
@login_required
def IndexView(request):
    activeIndex = "active"
    # 从个人文档中筛选出上传者和当前用户一致的文档
    user_id = request.user.id
    # 所有文档个数
    allFiles = File.allFiles.count()
    # 所有公开文档总量
    publicFiles = File.publicFiles.count()
    # 所有公开文档的大小总和
    allSize = File.allFiles.get_size_sum()
    # 项目个数
    allProjects = Project.allProjects.count()
    # 项目文档数
    projectFiles = File.projectFiles.count()# 项目ID不为空则是项目文件
    #allFiles = File.publicFiles.filter(project__id=u'').count()
    return render_to_response('app_filemanager/index.html', context_instance=RequestContext(request,locals()))

@login_required
def UploadView(request):
    #-----------------------
    #-----------------------
    activeUpload = "active"
    if request.method == 'GET':
        form = FileForm(
            user=request.user,
            initial = {
                'public': '1',
                'deleted': '0',
            },
        )
        return render_to_response('app_filemanager/upload.html', context_instance=RequestContext(request,locals()))
    else:
        form = FileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            f = File.allFiles.create(
                file = request.FILES['file'],
                public = form.cleaned_data['public'],
                project = form.cleaned_data['project'],
                uploader = User.objects.get(username = request.user.username), 
                deleted = form.cleaned_data['deleted'],
                desc = form.cleaned_data['desc'],
                upload_date = datetime.datetime.now(),
                change_date = datetime.datetime.now(),
                tag = form.cleaned_data['tag'],
            )
            group = form.cleaned_data['group']
            for g in group:
                f.group.add(g)
            f.save()
            return render_to_response('app_filemanager/success.html', context_instance=RequestContext(request,locals()))
        else:
            return render_to_response('app_filemanager/upload.html', context_instance=RequestContext(request,locals()))

def ListPersonalView(request):
    activePersonalList = "active"
    if not request.user.has_perm('app_filemanager.can_list_file'):
        return render_to_response('app_filemanager/noperm.html', context_instance=RequestContext(request,locals()))
    else: 
        user_name = request.user.id
	# {{ new_upload_file }}in template
        privateFiles = File.privateFiles.filter(
            uploader=user_name
        ).order_by('-upload_date')
        
        publicFiles = File.publicFiles.filter(
            uploader=user_name
        ).order_by('-upload_date')
        projectFiles = File.allFiles.filter(
            uploader=user_name,
            project__isnull=False
	# 这里的uploader
        ).order_by('-upload_date')
	    #upload_date__lte = timezone.now()
	    #upload_date__lte = datetime.datetime.utcnow().replace(tzinfo=utc)
    return render_to_response('app_filemanager/listPersonal.html', context_instance=RequestContext(request,locals()))

# -------------------------------list------------------
from django.db.models import Count
def ListProjectView(request):
    activePublicList = "active"
    if not request.user.has_perm('app_filemanager.can_list_file'):
        return render_to_response('app_filemanager/noperm.html', context_instance=RequestContext(request,locals()))
    else: 
        user_name = request.user.id
        # 为publicprojects附加一个projects__count对象来获得每个project有几个File
        # 返回公开的项目的queryset
        allProjects = Project.allProjects.all().annotate(Count('projects'))
        recentUploadFile = File.projectFiles.all().order_by('-upload_date')[:4]
    return render_to_response('app_filemanager/listProject.html', context_instance=RequestContext(request,locals()))

def GlobleView(request):
    publicprojects = Project.publicProjects.all().annotate(Count('projects'))
    recentUploadFile = File.projectFiles.all().order_by('-upload_date')[:4]
    return {
        'publicprojects': publicprojects,
        'recentUploadFile': recentUploadFile,
    }
    
def ListAllProjectFileView(request):
    activePublicList = "active"
    allprojectfile = File.projectFiles.all().order_by('-upload_date')
    return render_to_response('app_filemanager/listAllProjectFile.html', context_instance=RequestContext(request,locals()))
def ListProjectFileView(request, project_id):
    activePublicList = "active"
    theproject = Project.publicProjects.get(id=project_id)
    projectFiles = File.projectFiles.filter(project = project_id).order_by('-upload_date')
    dict = {}
    for o in projectFiles:
        o.active_field = "active"
    return render_to_response('app_filemanager/listProjectFile.html', context_instance=RequestContext(request,locals()))

def ListPublicFileView(request):
    activePublicList = "active"
    publicFiles = File.publicFiles.all().order_by('-upload_date')
    return render_to_response('app_filemanager/listPublicFile.html', context_instance=RequestContext(request,locals()))

# -----------------------------detail-------------
def FileDetailView(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file_type=mimetypes.guess_type(file.file.url)[0]
    return render_to_response('app_filemanager/filedetail.html', context_instance=RequestContext(request,locals()))
def FileDetailView_no_edit(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file_type=mimetypes.guess_type(file.file.url)[0]
    return render_to_response('app_filemanager/filedetail_no_edit.html', context_instance=RequestContext(request,locals()))

def ProjectDetailView(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render_to_response('app_filemanager/projectdetail.html', context_instance=RequestContext(request,locals()))


@login_required
def DownloadView(request, file_id):
    x = get_object_or_404(File, pk=file_id)
    if request.user.id == 1:
        name = x.file.name.split('/').pop()
        wrapper=FileWrapper(x.file) 
        content_type=mimetypes.guess_type(x.file.url)
        response=HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = x.file.size
        print sys.getdefaultencoding()
        response['Content-Disposition']="attachment;filename=%s" % str(name) 
        return response
    elif not (request.user.has_perm('app_filemanager.can_download_file') or request.user.id == x.uploader.id):
            return render_to_response('app_filemanager/noperm.html', context_instance=RequestContext(request,locals()))
    else:
        name = x.file.name.split('/').pop()
        wrapper=FileWrapper(x.file)
        content_type=mimetypes.guess_type(x.file.url)
        response=HttpResponse(wrapper,content_type=content_type)
        response['Content-Length'] = x.file.size
        print sys.getdefaultencoding()
        response['Content-Disposition']='attachment;filename=%s' % str(name)
        return response

def LogoutView(request):
    logout(request)
    return HttpResponseRedirect("/file")

@login_required
def UserProfileView(request):
    return render_to_response('app_filemanager/userprofile.html', context_instance=RequestContext(request,locals()))
# -------------------------------create
class ProjectCreateView(CreateView):
    model = Project
    success_url = '/file/list/project/'
# -------------------------------update
class FileUpdateView(UpdateView):
    model = File
    template_name_suffix = '_update_form'
    success_url = '/file/list/personal/'
    permission_required = 'app_filemanager.can_change_file'
    permission_fail_message = ('You don\'t have permission to change employee info.')
    form_class = FileForm
    def get_form_kwargs(self):
        kwargs = super(FileUpdateView, self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs

    # 限制只能修改本人上传的文件
    def get_queryset(self):
        base_qs = super(FileUpdateView, self).get_queryset()
        return base_qs.filter(uploader=self.request.user)

class ProjectUpdateView(UpdateView):
    model = Project
    template_name_suffix = '_update_form'
    success_url = '/file/list/project/'
    permission_required = 'app_filemanager.can_change_file'
    permission_fail_message = ('You don\'t have permission to change employee info.')
    form_class = ProjectForm

class DeleteFileView(DeleteView):
    model = File
    success_url = '/file/list/personal/'

def SearchView(request):
    #if not request.user.has_perm('app_filemanager.can_see'):
    #    return render_to_response('app_filemanager/noperm.html', context_instance=RequestContext(request,locals()))
    #else:
    text = request.GET.get('searchtext', '')
    user_id = request.user.id
    #file = get_list_or_404(File,file__icontains=text, uploader=user_id)
    searchFiles = File.allFiles.filter(file__icontains=text)
    return render_to_response('app_filemanager/searchResult.html', context_instance=RequestContext(request,locals()))
"""
def SearchView(request):
    if not request.user.has_perm('app_filemanager.can_see'):
        return render_to_response('app_filemanager/noperm.html', context_instance=RequestContext(request,locals()))
    else:
        text = request.GET.get('searchtext', '')
        user_id = request.user.id
        #file = get_list_or_404(File,file__icontains=text, uploader=user_id)
        file = File.objects.filter(file__icontains=text,uploader=user_id)
        return render_to_response('app_filemanager/listPersonal.html', context_instance=RequestContext(request,locals()))
demo:

username = request.session.get('login_user', False)

if user.auth_group in args or user.auth_group == 'admin':

def my_view(request):
    if not (request.user.is_authenticated() and request.user.has_perm('polls.can_vote')):
        return HttpResponse("You can't vote in this poll.")

{% if perms.foo %} # foo为应用名，并非model名
  <p>你有操作foo的权限。</p>
  {% if perms.foo.can_vote %}
    <p>你可以投票。</p>
  {% endif %}
  {% if perms.foo.can_drive %}
    <p>你可以开车。</p>
  {% endif %}
{% else %}
  <p>你没有操作foo的权限。</p>
{% endif %}

"""
