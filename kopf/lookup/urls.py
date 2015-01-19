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
        url(r'^zero/$',views.sample_zero_view,name='zero'),
        
        url(r'^abdb/$',views.abdb, name='antibodyDB'),
        url(r'^add_ab/$',views.add_ab, name='add_ab'),
        url(r'^deleteAB/(?P<pk>.*)$',views.deleteAB, name='remove_ab'),
        
        url(r'^kits/$', views.kit, name='kit'),
                       #url(r'^add_kit/$',views.add_kit, name='add_kit'),
        url(r'^add/$',views.add, name='add'),
        url(r'^removekit/$',views.removekit, name='removekit'),
        url(r'^reactkit/(?P<pk>.*)$',views.reactkit, name='reactkit'),
                       #url(r'^update_kit/$',views.update_kit, name='update_kit'),
        url(r'^update/$',views.update, name='update'),
        url(r'^upload_file/$',views.upload_file, name='upload_file')
    )