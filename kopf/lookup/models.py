from django.db import models

class Annotation(models.Model):
    scientist = models.CharField(max_length=200)
    sample = models.CharField(max_length=10)
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



