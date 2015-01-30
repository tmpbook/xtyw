#coding=utf8
from django.db import models
from django.contrib.auth.models import User, Group
# 类顺序不可改变
class AllProjectManager(models.Manager):
    def get_queryset(self):
        return super(AllProjectManager, self).get_queryset().all()

class CloseProjectManager(models.Manager):
    def get_queryset(self):
        return super(CloseProjectManager, self).get_queryset().filter(public=False)

class PublicProjectManager(models.Manager):
    def get_queryset(self):
        return super(PublicProjectManager, self).get_queryset().filter(public=True)

"""
class PublicProjctManager(models.Manager):
    def get_public_project(self, user):
        return self.get_query_set().filter(user=user, public=True)
# 通过用户获得拥有的且公开的项目，用法：
Project.objects.get_public_project(user=user)
"""
class Project(models.Model):
    name = models.CharField(max_length=50)
    public = models.BooleanField(default=True)
    add_date = models.DateTimeField(auto_now_add=True)
    end_data = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User)
    desc = models.TextField(blank=True, null=True)
    # Manager blow:
    allProjects = AllProjectManager()
    closeProjects = CloseProjectManager()
    publicProjects = PublicProjectManager()

    def __unicode__(self):
        return self.name
    class Meta:
        permissions = (
            ('can_edit_project', "能编辑项目"),
            ('can_delete_project', "能删除项目"),
            ('can_add_project', "能添加项目"),
        )

class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class AllFileManager(models.Manager):
    def get_queryset(self):
        return super(AllFileManager, self).get_queryset().all()

class PrivateFileManager(models.Manager):
    def get_queryset(self):
        return super(PrivateFileManager, self).get_queryset().filter(public=False, deleted=False)
        
class PublicFileManager(models.Manager):
    def get_queryset(self):
        return super(PublicFileManager, self).get_queryset().filter(public=True, deleted=False)

class ProjectFileManager(models.Manager):
    def get_queryset(self):
        return super(ProjectFileManager, self).get_queryset().filter(deleted=False, project__isnull=False)

from django.template.defaultfilters import slugify
class File(models.Model):
    def makefilename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        slug = slugify(fname)
        return '%s.%s' % (slug, extension)
    file = models.FileField(upload_to=makefilename)
    public = models.BooleanField()# has default
    project = models.ForeignKey(Project, related_name="projects", blank=True, null=True)
    tag = models.ForeignKey(Tag, related_name="tags")
    uploader = models.ForeignKey(User, related_name="users")
    group = models.ManyToManyField(Group, related_name="groups")
    deleted = models.BooleanField()# has default
    desc = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    
    # Managers blow:
    allFiles = AllFileManager()
    privateFiles = PrivateFileManager()
    publicFiles = PublicFileManager()
    projectFiles = ProjectFileManager()    
    

    def __unicode__(self):
        return self.file.name
    class Meta:
        permissions = (
            ("can_edit_file", "能编辑文件"),
            ("can_list_file", "能看文件列表"),
            ("can_delete_file", "能删除文件"),
            ("can_download_file", "能下载文件"),
        )
'''
-----------------------------------------------------------------------------------------------
One-to-many relationships

>>> b = File.objects.get(id=1)
>>> b.projects.all() # Returns all Entry objects related to File.

# b.projects is a Manager that returns QuerySets.
>>> b.projects.filter(headline__contains='一期')
>>> b.projects.count()
-----------------------------------------------------------------------------------------------
Many-to-many relationships

e = Entry.objects.get(id=3)
e.authors.all() # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains='John')

a = Author.objects.get(id=5)
a.entry_set.all() # Returns all Entry objects for this Author.
-----------------------------------------------------------------------------------------------
>>> import copy
>>> manager = MyManager()
>>> my_copy = copy.copy(manager)
------------------------------------------------------------------------------------------------
'''
