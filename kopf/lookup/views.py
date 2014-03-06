from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world! <a href='/lookup/about'>About</a>")

def about(request):
    return HttpResponse("About")


# Create your views here.
