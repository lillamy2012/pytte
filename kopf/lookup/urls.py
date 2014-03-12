from django.conf.urls import patterns, url
from lookup import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<sample_id>\d+)/details/$', views.detail, name='detail'),
        url(r'^(?P<sample_id>\d+)/results/$', views.results, name='results'),
        url(r'^about/', views.about, name='about'),
        url(r'^projects/', views.projects, name='projects'))
        url(r'^genotype/', views.genotype, name='genotype'))