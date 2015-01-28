#coding=utf-8
from django.conf.urls import patterns,url
from app_filemanager import views


urlpatterns=patterns('',
    url(r'^$',views.IndexView, name='index'),
    url(r'^upload/$', views.UploadView, name='upload'), 
    # list file & project
    url(r'^list/personal/$', views.ListPersonalView, name='listPersonal'),
    url(r'^list/project/$', views.ListProjectView, name='listProject'),
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
    #url(r'search/$',views.SearchView, name='search'), 
)
