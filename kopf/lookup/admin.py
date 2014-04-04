from django.contrib import admin
from lookup.models import Annotation, ProjectBlogg, BlogAdmin, Project

admin.site.register(Annotation)
admin.site.register(Project)
admin.site.register(ProjectBlogg, BlogAdmin)

# Register your models here.
