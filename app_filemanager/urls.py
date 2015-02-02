#coding=utf-8
from django.conf.urls import patterns,url
from app_filemanager import views


urlpatterns=patterns('',
    url(r'^$',views.IndexView, name='index'),
    # create file & project
    url(r'^create/project/$', views.ProjectCreateView.as_view(), name='createproject'),
    url(r'^upload/$', views.UploadView, name='upload'), 
    # list file & project
    url(r'^list/personal/$', views.ListPersonalView, name='listPersonal'),
    url(r'^list/project/$', views.ListProjectView, name='listProject'),
    url(r'^list/allprojectfile/$', views.ListAllProjectFileView, name='listAllProjectFile'),
    url(r'^list/allpublicfile/$', views.ListPublicFileView, name='listPublicFile'),
    # detail file & project
    url(r'^detail/fileid=(?P<file_id>\d+)/$', views.FileDetailView, name='filedetail'), 
    url(r'^detail/projectid=(?P<project_id>\d+)/$', views.ProjectDetailView, name='projectdetail'),
    # update file & project
    url(r'^file/update/fileid=(?P<pk>\d+)/$', views.FileUpdateView.as_view(), name='fileupdate'),
    url(r'^project/update/projectid=(?P<pk>\d+)/$', views.ProjectUpdateView.as_view(), name='projectupdate'),
    # list file of each project
    url(r'^list/projectfile/projectid=(?P<project_id>\d+)$', views.ListProjectFileView, name='listProjectfile'),
    # down file
    url(r'^download/fileid=(?P<file_id>\d+)/$',views.DownloadView,name='download'), 
    # delete file
    url(r'^delete/fileid=(?P<pk>\d+)/$', views.DeleteFileView.as_view(), name='deletefile'),
    #url(r'search/$',views.SearchView, name='search'), 
)
