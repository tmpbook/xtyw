from django.conf.urls import patterns, include, url
from app_filemanager import views
# -------------------------------------------------------
from django.contrib import admin
from app_filemanager.api import ProjectResource
entry_resource = ProjectResource()
# -------------------------------------------------------
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.IndexView, name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(entry_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^file/',include('app_filemanager.urls', namespace="file")),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout$', views.LogoutView, name="logout"),
    url(r'^accounts/profile/$', views.UserProfileView),
)
