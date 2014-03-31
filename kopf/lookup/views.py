from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from lookup.models import Annotation, Project, Scientist
from django.core import serializers
from django.forms.models import model_to_dict
from itertools import chain

def index(request):
    context = RequestContext(request)
    nproj = len(Project.objects.values_list('project_name').distinct())
    nscient = len(Annotation.objects.values_list('scientist').distinct())
    nsamples= len(Annotation.objects.values_list('sample').distinct())
    context_dict = {'scientist':nscient,'samples':nsamples,'projects':nproj}
    return render_to_response('lookup/index.html', context_dict, context)

def about(request):
    return render(request, 'lookup/about.html')

def detail(request):
    sample_id = request.GET.get('id')
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

def genotype(request):
    nproj = list(Annotation.objects.values_list('genotype').distinct())
    return render(request, 'lookup/genotype.html',{'genotypes': nproj})

def antibody(request):
    nproj = list(Annotation.objects.values_list('antibody').distinct())
    return render(request, 'lookup/antibody.html',{'genotypes': nproj})

def tissue(request):
    nproj = list(Annotation.objects.values_list('genotype').distinct())
    return render(request, 'lookup/tissue.html',{'genotypes': nproj})

def user(request,sc_id):
    try:
        sc = Scientist.objects.get(name=sc_id)
    except Scientist.DoesNotExist:
        raise Http404
    data =model_to_dict(Scientist.objects.filter(name=sc_id)[0])
    return render(request, 'lookup/user.html', {'Scientist': sc, 'ListL': data})

def scientists(request):
    sc=Scientist.objects.all()
    ll={}
    for i in sc:
        ll[i]=len(Annotation.objects.filter(scientist=i))
    
    return render(request, 'lookup/scientists.html', {'Scientist': ll, 'people': Scientist.objects.all()})

def allsamples(request):
    ann = serializers.serialize("python", Annotation.objects.all(),fields=('sample','scientist','antibody','genotype'))
    #pr =  serializers.serialize("python",Project.objects.all(),fields=('samples'))

    pr = Project.objects.values_list('project_name').distinct()
    return render(request, 'lookup/allsamples.html',{'Annotation': ann, 'Project': pr})

def cross_corr(request):
    return render(request,'lookup/croos_corr.html')

