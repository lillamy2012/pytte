from django.db import models

class Annotation(models.Model):
    scientist = models.CharField(max_length=200)
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
        return self.scientist

    def get_fields(self):
        return self._meta.get_all_field_names()

    def get_entry(self,field):
       return self._meta.get_field(field).verbose_name#this will get the field
        
        

class Project(models.Model):
    primary_scientist = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200,primary_key=True)
    samples = models.ManyToManyField(Annotation)

    def __unicode__(self):
        return self.project_name