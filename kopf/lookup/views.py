from django.core import serializers
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.models import model_to_dict
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from lookup.models import Annotation, Project, Scientist, ProjectBlogg, CommentForm, Stats, Antibody, AntibodyForm, DeleteABForm, KitForm, Kit, ProtocolDocForm, Protocol, Seed, SeedRelation, SeedForm,  Seed1stForm
from itertools import chain
from chartit import DataPool, Chart, PivotDataPool, PivotChart
from django.db.models import Avg, Max, Count
from django.utils import simplejson
from django.core.mail import send_mail
from django.db import models
import os, re, string

#####################
### index page
#####################

def index(request):
    context = RequestContext(request)
    nproj = len(Project.objects.values_list('project_name').distinct())
    nscient = len(Annotation.objects.values_list('scientist').distinct())
    nsamples= len(Annotation.objects.values_list('sample').distinct())
    
    nkitt= len(Kit.objects.values_list('name').distinct().filter(active=True))
    nkitf= len(Kit.objects.values_list('name').distinct().filter(active=False))
    
    nantit = len(Antibody.objects.filter(active=True))
    nantif = len(Antibody.objects.filter(active=False))
                 
    context_dict = {'scientist':nscient,'samples':nsamples,'projects':nproj, 'nkitt': nkitt , 'nkitf': nkitf ,'nantit': nantit, 'nantif' : nantif}
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
    type = getattr(ann, 'exptype')
    data =model_to_dict(Annotation.objects.filter(sample=sample_id)[0])
    try:
        proj=Project.objects.get(samples=sample_id)
        res =  {'Annotation': ann, 'ListL': data, 'exp':type, 'project':proj}
    except Project.DoesNotExist:
        res =  {'Annotation': ann, 'ListL': data, 'exp':type}
    try:
        sta=Stats.objects.get(sample=sample_id)
        stat=model_to_dict(Stats.objects.filter(sample=sample_id)[0])
        res['Stats'] = stat
    except Stats.DoesNotExist:
        res = res
    return render(request, 'lookup/detail.html', res)

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
    RNA = serializers.serialize("python", Annotation.objects.filter(exptype="RNA-Seq"),fields=('sample','scientist','genotype'))
    CHIP = serializers.serialize("python", Annotation.objects.filter(exptype="ChIP-Seq"),fields=('sample','scientist','antibody','genotype'))
    pr = Project.objects.values_list('project_name').distinct()
    return render(request, 'lookup/allsamples.html',{'RNAanno': RNA,'ChipAnno': CHIP, 'Project': pr})

########################
## Stats
########################

def cross_corr(request):
    return render(request,'lookup/croos_corr.html')

#######################
### Projects - list all projects
#######################

def projects(request):
    posts = Project.objects.all() #.order_by("-project_name")
    a = Project.objects.values_list('samples').distinct()
    scientist = Project.objects.values()
    return render(request, 'lookup/projects.html', {'Projectnames': posts,'Projects': scientist})


########################
## Blog
########################
### will become projects and removed
#def blog(request):
#   pk = request.GET.get('project')
#   posts = Project.objects.all().order_by("-project_name")
#   paginator = Paginator(posts, 2)
#   try:
#       page = int(request.GET.get("page", '1'))
#   except ValueError: page = 1
#   try:
#       posts = paginator.page(page)
#   except (InvalidPage, EmptyPage):
#       posts = paginator.page(paginator.num_pages)
#   return render_to_response("lookup/blog.html", dict(posts=posts, user=request.user))

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

###
##########

def sample_chart_view(request):
   return render_to_response("lookup/test.html")

def my_ajax_view(request):
    nproj2 = list(Annotation.objects.values_list('scientist').distinct())
    data_dict = []
    for i in nproj2:
        l = len(Annotation.objects.filter(scientist=i, exptype="RNA-Seq"))
        t = {'scientist':i ,  "status":"RNA", "val":l}
        data_dict.append(t)
        l = len(Annotation.objects.filter(scientist=i, exptype="ChIP-Seq"))
        t = {'scientist':i ,  "status":"ChIP", "val":l}
        data_dict.append(t)
        l = len(Annotation.objects.filter(scientist=i, exptype="Other"))
        t = {'scientist':i ,  "status":"Other", "val":l}
    return HttpResponse(simplejson.dumps(data_dict),mimetype='application/json')

###
#######

def sample_zero_view(request):
    nproj2 = (list(Stats.objects.values_list('zeroReads')))
    
    return HttpResponse(simplejson.dumps(nproj2),mimetype='application/json')


################################################
################################################
def seed(request):
    type = request.GET.get('type')
    seedentry = serializers.serialize("python",Seed.objects.all())
    return render(request, 'lookup/seed.html',{'Seeds' : seedentry, 'type':type})


def addnewseed(request):
    form = Seed1stForm()
    if request.method == "POST":
        form = Seed1stForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lookup/addnewseed/')
        else:
            return render(request, 'lookup/valab.html',{'form' : form } )

    else:
        return render(request, 'lookup/addnewseed.html',{'form' : form } )


def addseed(request):
    ps = request.GET.getlist('parents')
    ll = len(ps)
    if ll > 2:
        return HttpResponse("You have selected more than two plants, please go back (use the browser's back arrow) and correct it. ")
    if ll == 1:
        return HttpResponse("You have selected only one plant, please go back (use the browser's back arrow) and correct it. ")
    if ll == 0:
        return HttpResponse("You need to selected two plants to cross, please go back (use the browser's back arrow) and correct it. ")
    parent1 = Seed.objects.get(pk=ps[0])
    parent2 = Seed.objects.get(pk=ps[1])
    new=Seed()
    if parent1.type == parent2.type :
        new.type = parent1.type
    else:
        new.type = parent2.type + " " + parent1.type
    if parent1.linename == parent2.linename :
        new.linename = parent1.linename
    else:
        new.linename = parent2.linename + " " + parent1.linename
    if parent1.ecotype == parent2.ecotype :
        new.ecotype = parent1.ecotype
    else:
        new.ecotype = parent2.ecotype + " " + parent1.ecotype
    form = SeedForm(instance=new,prefix='main')
    if request.method == "POST":
        form = SeedForm(request.POST,instance=new,prefix='main')
        if form.is_valid():
            form.save()
            rel = SeedRelation(offspring=new,parent=parent1)
            rel.save()
            rel = SeedRelation(offspring=new,parent=parent2)
            rel.save()
            return redirect('/lookup/seed/')
        else:
            return render(request, 'lookup/valab.html',{'form' : form } )
    else:
        return render(request,'lookup/addseed.html', { 'form' :  form , 'p1' : ps[0] , 'p2' : ps[1] } )


def seeparents(request,pk):
    p = SeedRelation.objects.filter(offspring=pk)
    my_list = p.values_list('parent', flat=True)
    pss = Seed.objects.filter(pk__in=my_list)
    ps= serializers.serialize("python",pss)
    return render(request, 'lookup/seeparents.html',{'ps' : ps , 'my_list' : my_list} )

################################################
## abdb


def antibody(request):
    sample_type = request.GET.get('type')
    #proto = serializers.serialize("python",Protocol.objects.all())
    if not sample_type or sample_type == 'None':
        antibody = serializers.serialize("python",Antibody.objects.filter(active=True))
    else:
        if sample_type=="inact":
           antibody = serializers.serialize("python",Antibody.objects.filter(active=False))
        if sample_type=="com":
            antibody = serializers.serialize("python",Antibody.objects.exclude(company__isnull=True).exclude(company__exact=''))
        if sample_type=="home":
            antibody = serializers.serialize("python",Antibody.objects.filter(company__exact=''))
    return render(request, 'lookup/antibody.html',{'Antibody' : antibody, 'type' : sample_type}) #, 'proto' : proto})


def addab(request):
    form = AntibodyForm(initial={'antibody-active':True },prefix="antibody")
    #prform = ProtocolDocForm(prefix="proto")
    if request.method == "POST":
        cf = AntibodyForm(request.POST,prefix="antibody")
        val = cf.is_valid()
        if val == False:
            #return HttpResponse({)
            #return redirect('/lookup/addab/')
            return render(request, 'lookup/valab.html',{'form' : cf } )
        #return render(request, 'lookup/valab.html',{'form' : form })
        else:
            anti = cf.save(commit=False)
            anti.save()
            #send_mail('kit added to lab db', 'hello, this just to inform you that a kit named "%s" been added to the kit db' % (kit.pk), 'elinaxel@gmail.com', ['elin.axelsson@gmi.oeaw.ac.at'])
            #prform = ProtocolDocForm(request.POST, request.FILES,prefix="proto")
            #if prform.is_valid():
            #   newlink = Protocol(kit=kit,doc = request.FILES['proto-doc'],name=kit.pk)
            #   newlink.save()
        return redirect('/lookup/addab/')
    else:
        return render(request, 'lookup/addab.html',{'form' : form } )


#Make antibody inactive (eg, not currently availible)

def inactanti(request):
    pk = request.GET.get('pk')
    type = request.GET.get('type')
    anti_to_inactivate = Antibody.objects.get(pk=pk)
    anti_to_inactivate.active = False
    anti_to_inactivate.save()
    # email
    return redirect('/lookup/antibody/?type='+str(type))

#Make kit active (eg, new order recieved)

def reactanti(request,pk):
    anti_to_activate = Antibody.objects.get(pk=pk)
    anti_to_activate.active = True
    anti_to_activate.save()
    # email
    return redirect('/lookup/antibody/?type=inact')


def updateab(request):
    pk = request.GET.get('pk')
    type = request.GET.get('type')
    instance = Antibody.objects.get(pk=pk)
    if request.method == "POST":
        form = AntibodyForm(request.POST, instance=instance)
        val = form.is_valid()
        if val == False:
            return HttpResponse("Some of the data is not valid, please go back (use the browser's back arrow) and correct it. ")

        else:
            anti = form.save(commit=False)
            anti.save()
        #send_mail('kit in lab db updated', 'hello, this just to inform you that the kit "%s" has been updated in the kit db' % (pk), 'elinaxel@gmail.com', ['elin.axelsson@gmi.oeaw.ac.at'])
        return redirect('/lookup/antibody/?type='+str(type))
    else:
        form = AntibodyForm(instance=instance)
        return render(request, 'lookup/updateab.html',{'form' : form , 'pk' :pk, 'type' : type })




##############################################################################################
#def send_update_mail(request):


##############################################################################################

#Show kits of some type or all

def kit(request):
    sample_type = request.GET.get('type')
    proto = serializers.serialize("python",Protocol.objects.all())
    if not sample_type or sample_type == 'None':
        kits = serializers.serialize("python",Kit.objects.filter(active=True))
    else:
        if sample_type=="inact":
            kits = serializers.serialize("python",Kit.objects.filter(active=False))
        else:
            kits = serializers.serialize("python",Kit.objects.filter(kittype=sample_type,active=True))
    return render(request, 'lookup/kits.html',{'Kits' : kits , 'type' : sample_type, 'proto' : proto})

#Add new kit

def add(request):
    form = KitForm(initial={'kit-active':True },prefix="kit")
    prform = ProtocolDocForm(prefix="proto")
    if request.method == "POST":
        cf = KitForm(request.POST,prefix="kit")
        val = cf.is_valid()
        if val == False:
           return HttpResponse("Some of the data is not valid. Maybe the date is not in the correct format (YYYY-MM-DD) or you have used the same name as an existing kit. The date can be corrected by using the browser's back arrow. If you want to edit an existing kit please do this using the 'edit kit' link in the kit overview list ")
        else:
            kit = cf.save(commit=False)
            kit.save()
            send_mail('kit added to lab db', 'hello, this just to inform you that a kit named "%s" been added to the kit db' % (kit.pk), 'elinaxel@gmail.com', ['elin.axelsson@gmi.oeaw.ac.at'])
            prform = ProtocolDocForm(request.POST, request.FILES,prefix="proto")
            if prform.is_valid():
                newlink = Protocol(kit=kit,doc = request.FILES['proto-doc'],name=kit.pk)
                newlink.save()
        return redirect('/lookup/add/')
    else:
        return render(request, 'lookup/add.html',{'form' : form , 'prform' : prform } )



#Update information, existing kit

def update(request):
    pk = request.GET.get('pk')
    type = request.GET.get('type')
    instance = Kit.objects.get(pk=pk)
    if request.method == "POST":
        form = KitForm(request.POST, instance=instance)
        val = form.is_valid()
        if val == False:
            return HttpResponse("Some of the data (eg the date) is not valid, please go back (use the browser's back arrow) and correct it. ")
        else:
            kit = form.save(commit=False)
            kit.save()
            send_mail('kit in lab db updated', 'hello, this just to inform you that the kit "%s" has been updated in the kit db' % (pk), 'elinaxel@gmail.com', ['elin.axelsson@gmi.oeaw.ac.at'])
        return redirect('/lookup/kits/?type='+str(type))
    else:
        form = KitForm(instance=instance)
        return render(request, 'lookup/update.html',{'form' : form , 'pk' :pk, 'type' : type })

#Make kit inactive (eg, not currently availible)

def removekit(request):
    pk = request.GET.get('pk')
    type = request.GET.get('type')
    kit_to_inactivate = Kit.objects.get(pk=pk)
    kit_to_inactivate.active = False
    kit_to_inactivate.save()
    # email
    return redirect('/lookup/kits/?type='+str(type))

#Make kit active (eg, new order recieved)

def reactkit(request,pk):
    kit_to_activate = Kit.objects.get(pk=pk)
    kit_to_activate.active = True
    kit_to_activate.save()
    # email
    return redirect('/lookup/kits/?type=inact')


##############################################################################################




def upload_file(request):
    pk = request.GET.get('pk')
    kit_to_use = Kit.objects.get(pk=pk)
    if request.method == "POST":
        form = ProtocolDocForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                os.remove(os.path.join('lookup/static/protocol',"%s.%s" % (kit_to_use.pk,"pdf")))
            except:
		pass
	    newlink = form.save(commit=False)
            newlink.kit = kit_to_use
            newlink.name = kit_to_use.pk
            newlink.save()
            #a = "%s" %
            send_mail('new protocol uploaded', 'hi, this just to inform you that kit "%s" has been assigned a new protocol in the lab db' % (pk), 'elinaxel@gmail.com', ['elin.axelsson@gmi.oeaw.ac.at'])
            return redirect('/lookup/kits/')
        else:
            return  HttpResponse("file was not valid")
    else:
        form = ProtocolDocForm(instance=kit_to_use)
        return render_to_response('lookup/upload.html', {'form': form, 'pk' : pk }, context_instance=RequestContext(request))




