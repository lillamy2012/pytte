from django.http import HttpResponse
#from django.template import Context
#from django.template.loader import get_template
#from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from lookup.models import Annotation

def index(request):
    context = RequestContext(request)
    
    annotation_list = Annotation.objects.order_by('?')[:5]
    context_dict = {'annotations': annotation_list}
    
    return render_to_response('lookup/index.html', context_dict, context)

def about(request):
    return HttpResponse("About <a href='/lookup/'>Index</a>" )


# Create your views here.
