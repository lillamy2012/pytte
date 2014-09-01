from django.conf.urls import patterns, url
from lookup import views



urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^project_blog/(?P<pk>.*)$', views.project, name='project'),
        url(r'^blog/$', views.blog, name='blog'),
        url(r'^about/', views.about, name='about'),
        url(r'^projects/', views.projects, name='projects'),
        url(r'^genotype/', views.genotype, name='genotype'),
        url(r'^antibody/', views.genotype, name='antibody'),
        url(r'^tissue/', views.genotype, name='tissue'),
        url(r'^scientists/', views.scientists, name='scientists'),
        url(r'^allsamples/', views.allsamples,name='allsamples'),
        url(r'^details/$', views.detail,name='detail'),
        url(r'^add_blog/(?P<pk>.*)$', views.add_blog,name='add_blog'),
        url(r'^croos_corr/',views.cross_corr,name='cross_corr'),
        url(r'^test',views.sample_chart_view,name='test'),
        url(r'^ajex/$',views.my_ajax_view,name='map'),
        url(r'^zero/$',views.sample_zero_view,name='zero'))