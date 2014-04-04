from django.core import serializers
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from lookup.models import Annotation, Project, Scientist, ProjectBlogg, CommentForm
from itertools import chain


#####################
### index page
#####################

def index(request):
    context = RequestContext(request)
    nproj = len(Project.objects.values_list('project_name').distinct())
    nscient = len(Annotation.objects.values_list('scientist').distinct())
    nsamples= len(Annotation.objects.values_list('sample').distinct())
    context_dict = {'scientist':nscient,'samples':nsamples,'projects':nproj}
    return render_to_response('lookup/index.html', context_dict, context)

######################
### about page
######################

def about(request):
    return render(request, 'lookup/about.html')

######################
### sample details
######################

def detail(request):
    sample_id = request.GET.get('id')
    try:
        ann = Annotation.objects.get(sample=sample_id)
    except Annotation.DoesNotExist:
        raise Http404
    data =model_to_dict(Annotation.objects.filter(sample=sample_id)[0])
    return render(request, 'lookup/detail.html', {'Annotation': ann, 'ListL': data})

######################
### Results (to be removed??)
######################

def results(request, sample_id):
    return HttpResponse("You're looking at the results of sample %s." % sample_id)

########################
### Annotations
########################

def genotype(request):
    nproj = list(Annotation.objects.values_list('genotype').distinct())
    return render(request, 'lookup/genotype.html',{'genotypes': nproj})

def antibody(request):
    nproj = list(Annotation.objects.values_list('antibody').distinct())
    return render(request, 'lookup/antibody.html',{'genotypes': nproj})

def tissue(request):
    nproj = list(Annotation.objects.values_list('genotype').distinct())
    return render(request, 'lookup/tissue.html',{'genotypes': nproj})

########################
### User (too be removed)
########################

def user(request,sc_id):
    try:
        sc = Scientist.objects.get(name=sc_id)
    except Scientist.DoesNotExist:
        raise Http404
    data =model_to_dict(Scientist.objects.filter(name=sc_id)[0])
    return render(request, 'lookup/user.html', {'Scientist': sc, 'ListL': data})

#########################
### Scientist
#########################

def scientists(request):
    sc=Scientist.objects.all()
    ll={}
    for i in sc:
        ll[i]=len(Annotation.objects.filter(scientist=i))
    return render(request, 'lookup/scientists.html', {'Scientist': ll, 'people': Scientist.objects.all()})

########################
### List of all samples
########################

def allsamples(request):
    ann = serializers.serialize("python", Annotation.objects.all(),fields=('sample','scientist','antibody','genotype'))
    #pr =  serializers.serialize("python",Project.objects.all(),fields=('samples'))

    pr = Project.objects.values_list('project_name').distinct()
    return render(request, 'lookup/allsamples.html',{'Annotation': ann, 'Project': pr})

########################
## Stats
########################

def cross_corr(request):
    return render(request,'lookup/croos_corr.html')

#######################
### Projects - list all projects
#######################

def projects(request):
    #nproj = Project.objects.values_list('project_name').distinct()
    posts = Project.objects.all() #.order_by("-project_name")
    a = Project.objects.values_list('samples').distinct()
    #pr = Project.objects.all()
    #scientist = model_to_dict(Annotation.objects.all())
    scientist = Project.objects.values()
    return render(request, 'lookup/projects.html', {'Projectnames': posts,'Projects': scientist})


########################
## Blog
########################
### will become projects and removed
def blog(request):
    pk = request.GET.get('project')
    posts = Project.objects.all().order_by("-project_name")
    paginator = Paginator(posts, 2)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    return render_to_response("lookup/blog.html", dict(posts=posts, user=request.user))

###########################
## Project blog page
###########################

def project(request,pk): ##
    post = Project.objects.get(pk=pk)
    comments = ProjectBlogg.objects.filter(project=post)
    p_samples = post.samples.values_list("sample")
    ann = Annotation.objects.filter(sample__in=p_samples)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user,Anno=ann)
    d.update(csrf(request))
    return render_to_response("lookup/project_blog.html", d)

###########################
## add comments
###########################

def add_blog(request,pk):
    post = Project.objects.get(pk=pk)
    p = request.POST
    if p.has_key("body") and p["body"]:
        comment = ProjectBlogg(project=Project.objects.get(pk=pk))
        cf = CommentForm(p, instance=comment)
        comment = cf.save(commit=False)
        comment.save()
    return(HttpResponseRedirect(reverse('lookup.views.project',args=(post.project_name,))))


      