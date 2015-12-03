from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django import forms
import uuid
import os
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.forms import widgets
from django.forms import TextInput
from django.forms import DateInput
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
    raw = models.CharField(max_length=200,blank=True)
    align = models.CharField(max_length=200,null=True)

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

###################
## Paths (sample)
#class Path(models.Model):
#   sample = models.ForeignKey(Annotation)
#   raw = models.CharField()
#   align = models.CharField()

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
    antigen_used = models.CharField(max_length=60,blank=True)
    antibody = models.CharField(max_length=20)
    source = models.CharField(max_length=20)
    concentration = models.CharField(blank=True,null=True,max_length=20)
    ig_type = models.CharField(max_length=10,blank=True)
    dilution_western = models.FloatField(blank=True,null=True)
    secondary_western = models.CharField(max_length=40,blank=True)
    protein_size = models.CharField(blank=True,max_length=30)
    company = models.CharField(blank=True,max_length=60)
    location_work = models.CharField(max_length=40)
    location_storage = models.CharField(max_length=40,blank=True)
    comment = models.TextField(blank=True)
    active = models.BooleanField(default=True)


class AntibodyForm(ModelForm):
    class Meta:
        model = Antibody
        widgets = {
            'location_work': TextInput(attrs={'placeholder' :'where is the open tube kept?'}),
            'location_storage': TextInput(attrs={'placeholder' :'where is the stock stored?'}),
            #'name': TextInput(attrs={'placeholder' :'please choose an unique name'}),
            'company': TextInput(attrs={'placeholder' :'selling company'}),
            'comment': TextInput(attrs={'placeholder' :'add any additional info about antibody'}),
            'antibody': TextInput(attrs={'placeholder' :'Antibody against?'}),
            'source': TextInput(attrs={'placeholder' :'e.g. "mouse mAb"'}),
            'antigen_used':TextInput(attrs={'placeholder' :'peptide, whole protein or domain'}),
            'protein_size': TextInput(attrs={'placeholder' :'e.g. "25 kDa"'}),
            'secondary_western': TextInput(attrs={'placeholder' :'e.g. "goat anti rabbit IgG 1000X" '}),
            'dilution_western': TextInput(attrs={'placeholder' :'numeric value e.g. 250 '}),
            'concentration': TextInput(attrs={'placeholder' :'e.g. "1 mg/ml" '}),
            'ig_type': TextInput(attrs={'placeholder' :'e.g. "ND"'}),
}



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
    Polymerase = 'Polymerase'
    Plasmid='Plasmid'
    Gel='Gel'
    qPCR ='qPCR'
    Purification = 'Purification'
    RNAseq = 'RNAseq'
    ChIPseq = 'ChIpsq'
    Race = 'Race'
    BIseq = 'BIseq'
    Restriction_enzyme = 'Restriction_enzyme'
    subtype_choice = (
    (Polymerase,'Polymerase'),
    (Plasmid,'Plasmid'),
    (Gel,'Gel'),
    (qPCR,'qPCR'),
    (Purification,'Purification'),
    (RNAseq,'RNAseq'),
    (ChIPseq,'ChIPseq'),
    (BIseq,'BIseq'),
    (Race,'Race'),
    (Restriction_enzyme,'Restriction_enzyme'),                      
    )
    kittype = models.CharField(max_length=10,choices=type_choice)
    subtype = models.CharField(max_length=20,choices=subtype_choice)
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=60,primary_key=True)
    company = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
    opened = models.DateTimeField()
    stock = models.BooleanField()
    active = models.BooleanField(default=True)


class KitForm(ModelForm):
    class Meta:
        model = Kit
        widgets = {
            'location': TextInput(attrs={'placeholder' :'where is it kept?'}),
            'name': TextInput(attrs={'placeholder' :'please choose an unique name'}),
            'company': TextInput(attrs={'placeholder' :'selling company'}),
            'comment': TextInput(attrs={'placeholder' :'add any additional info about kit'}),
            'opened': DateInput(format=('%Y-%m-%d'),attrs={'placeholder' :'YYYY-MM-DD'}),
}


def get_path_and_name(instance,filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.name, ext)
    return os.path.join('static/protocol', filename)


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Error message')


class Protocol(models.Model):
    kit = models.ForeignKey(Kit)
    name = models.CharField(max_length=60)
    doc = models.FileField(upload_to=get_path_and_name,validators=[validate_file_extension])


class ProtocolDocForm(forms.ModelForm):
    class Meta:
        model=Protocol
        fields=('doc',)
###### seed

class Seed(models.Model):
    type=models.CharField(max_length=100)
    linename=models.CharField(max_length=50)
    ecotype=models.CharField(max_length=50)
    source=models.CharField(max_length=50)
    selectionmark=models.CharField(max_length=50,null=True, blank=True)
    genotypeprimer=models.CharField(max_length=50,null=True, blank=True)
    location=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
#date=models.DateField()

class seedContact(models.Model):
    seed = models.ForeignKey(Seed)
    contact = models.CharField(max_length=50)


class SeedForm(ModelForm):
    class Meta:
        model = Seed


class Seed1stForm(ModelForm):
    class Meta:
        model = Seed
        TYPE_CHOICES = (('wt', 'WT'),('mutant', 'Mutant'),('transgene', 'Transgene'),)
        SELECT_CHOICES = (('CAN', 'CAN'),('HYG', 'HYG'),('BAS', 'BAS'),('BILLI','BILLI'),)
        ECO_CHOICES = (('Col','Col'),('Ler','Ler'),)
        widgets = {
        'type' : forms.Select(choices = TYPE_CHOICES,attrs={'size': len(TYPE_CHOICES)}),
        'ecotype' : forms.Select(choices = ECO_CHOICES,attrs={'size': len(ECO_CHOICES)}),
        'selectionmark' :  forms.Select(choices = SELECT_CHOICES, attrs={'size': len(SELECT_CHOICES)})
}


class SeedRelation(models.Model):
    offspring = models.ForeignKey(Seed,related_name='child')
    parent =  models.ForeignKey(Seed,related_name='parent')













