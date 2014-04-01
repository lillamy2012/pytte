from django.db import models
from django.contrib import admin
from django.forms import ModelForm

###############
## Scientist
###############
class Scientist(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    

    def __unicode__(self):
        return self.name

################
## Annotation (Sample)
################
class Annotation(models.Model):
    scientist = models.ForeignKey(Scientist)
    
    sample = models.IntegerField(primary_key=True)
    descr = models.CharField(max_length=200)
    genotype = models.CharField(max_length=10)
    comments = models.CharField(max_length=200)
    tissue_type = models.CharField(max_length=20)
    preparation_type = models.CharField(max_length=200)
    organism = models.CharField(max_length=20)
    celltype = models.CharField(max_length=20)
    antibody = models.CharField(max_length=20)

    def __unicode__(self):
        return self.sample

    def get_fields(self):
        return self._meta.get_all_field_names()

    def get_entry(self,field):
       return self._meta.get_field(field).verbose_name#this will get the field

################
## Project
################
class Project(models.Model):
    primary_scientist = models.ForeignKey(Scientist)
    project_name = models.CharField(max_length=200,primary_key=True)
    samples = models.ManyToManyField(Annotation)

    def __unicode__(self):
        return self.project_name

###############
##ProjectBlogg + Admin 
###############
class ProjectBlogg(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ManyToManyField(Scientist)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return unicode("%s: %s" % (self.project, self.body[:60]))



class BlogAdmin(admin.ModelAdmin):
    search_fields = ["title"]

class CommentForm(ModelForm):
    class Meta:
        model = ProjectBlogg
        exclude = ["project","owner"]
        

