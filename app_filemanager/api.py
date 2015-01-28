#conding=utf-8
from tastypie.resources import ModelResource  
  
from app_filemanager.models import Project
  
   
  
class ProjectResource(ModelResource):  
    class Meta:  
        queryset = Project.allProjects.all()  
        resource_name = 'project'
        #allowed_methods = ['get'] 
