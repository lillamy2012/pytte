from django.conf.urls import patterns, url
from lookup import views



urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<sample_id>\d+)/results/$', views.results, name='results'),
        url(r'^project_blog/$', views.project, name='project'),
        url(r'^blog/$', views.blog, name='blog'),
        url(r'^about/', views.about, name='about'),
        url(r'^projects/', views.projects, name='projects'),
        url(r'^genotype/', views.genotype, name='genotype'),
        url(r'^antibody/', views.genotype, name='antibody'),
        url(r'^tissue/', views.genotype, name='tissue'),
        url(r'^(?P<sc_id>.+)/user/$',views.user,name='user'),
        url(r'^scientists/', views.scientists, name='scientists'),
        url(r'^allsamples/', views.allsamples,name='allsamples'),
        url(r'^details/$', views.detail,name='detail'),
                       #url(r'^show-list/(?P<error_message>[\w_-]+)$', 'views.order_list'),
        url(r'^add_blog/', views.add_blog,name='add_blog'),
        url(r'^croos_corr/',views.cross_corr,name='cross_corr'))