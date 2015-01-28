from django.contrib import admin
from .models import Tag, File, Project
# Register your models here.

admin.site.register(Tag)
admin.site.register(File)
admin.site.register(Project)
