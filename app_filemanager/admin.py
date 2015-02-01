from django.contrib import admin
from .models import Tag, File, Project
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("owner", )
        form = super(TagAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register(Tag, TagAdmin)
admin.site.register(File)
admin.site.register(Project)
