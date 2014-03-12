#from django.http import HttpResponse
from django.http import Http404
#from django.template import Context
#from django.template.loader import get_template
#from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from lookup.models import Annotation, Project
from django.core import serializers
from django.forms.models import model_to_dict
from itertools import chain

def index(request):
    context = RequestContext(request)
    ## samples, type, scientist, genotypes
    nproj = len(Project.objects.values_list('project_name').distinct())
    nscient = len(Annotation.objects.values_list('scientist').distinct())
    nsamples= len(Annotation.objects.values_list('sample').distinct())
    context_dict = {'scientist':nscient,'samples':nsamples,'projects':nproj}
    return render_to_response('lookup/index.html', context_dict, context)

def about(request):
    return HttpResponse("About <a href='/lookup/'>Index</a>" )


def detail(request, sample_id):
    try:
        ann = Annotation.objects.get(sample=sample_id)
    except Annotation.DoesNotExist:
        raise Http404
    data =model_to_dict(Annotation.objects.filter(sample=sample_id)[0])
    return render(request, 'lookup/detail.html', {'Annotation': ann, 'ListL': data})


def results(request, sample_id):
    return HttpResponse("You're looking at the results of sample %s." % sample_id)


def projects(request):
    nproj = Project.objects.values_list('project_name').distinct()
    pr = Project.objects.all()
    #scientist = model_to_dict(Annotation.objects.all())
    scientist = Project.objects.values()
    return render(request, 'lookup/projects.html', {'Projectnames': nproj,'Projects': scientist})


#

                #def detail(request,sample_id):
#return render(request, 'lookup/detail.html', {'Annotation': Annotation.objects.get(sample_id)})

# Create your views here.
