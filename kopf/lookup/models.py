from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django import forms


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
    exptype = models.CharField(max_length=20)

    def __unicode__(self):
        return self.sample

    def get_fields(self):
        return self._meta.get_all_field_names()

    def get_entry(self,field):
       return self._meta.get_field(field).verbose_name#this will get the field

####################
## Stats (sample)
##################
class Stats(models.Model):
    sample = models.ForeignKey(Annotation)
    zeroReads = models.IntegerField()
    totReads = models.IntegerField()
    maxReads = models.IntegerField()


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

######################################################
######################################################

#################
# Antibody list
################
class Antibody(models.Model):
    antibody = models.CharField(max_length=60)
    comment = models.TextField()
    source = models.CharField(max_length=60)
    active = models.BooleanField(default=True)
   
def __unicode__(self):
    return unicode("%s: %s" % (self.antibody, self.comment[:60]))


class AntibodyForm(ModelForm):
    class Meta:
        model = Antibody


class DeleteABForm(ModelForm):
    class Meta:
        model = Antibody
        fields = []

#####################
## kits
#####################
class Kit(models.Model):
    RNA = 'RNA'
    DNA = 'DNA'
    Protein ='Protein'
    DeepSeq = 'DeepSeq'
    type_choice = (
    (RNA,'RNA'),
    (DNA,'DNA'),
    (Protein,'Protein'),
    (DeepSeq,'DeepSeq'),
    )
    Polymerase = 'pol'
    PCRpur='PCR'
    Plasmid='Plasmid'
    Gel='Gel'
    qPCR ='qPCR'
    RTPCR = 'RTPCR'
    RNApur = 'Rpu'
    RNAseq = 'Rsq'
    ChIPseq = 'Csq'
    BIseq = 'Bsq'
    subtype_choice = (
    (Polymerase,'Polymerase'),
    (PCRpur,'PCR'),
    (Plasmid,'Plasmid'),
    (Gel,'Gel'),
    (qPCR,'qPCA'),
    (RTPCR,'RTPCR'),
    (RNApur,'RNA purification'),
    (RNAseq,'RNAseq'),
    (ChIPseq,'ChIPseq'),
    (BIseq,'BIseq'),
    )
    kittype = models.CharField(max_length=10,choices=type_choice)
    subtype = models.CharField(max_length=10,choices=subtype_choice)
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=60)
    company = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
    opened = models.DateTimeField()
    protocol = models.CharField(max_length=60,blank=True)
    stock = models.BooleanField()
    active = models.BooleanField(default=True)


class KitForm(ModelForm):
    class Meta:
        model = Kit

class OutOfKitForm(ModelForm):
    class Meta:
        model = Kit
        fields = ['active']

class UpdateKitForm(ModelForm):
    somefield = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Kit



