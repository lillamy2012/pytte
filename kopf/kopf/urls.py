from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kopf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       #url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
                       #url(r'^about/', views.about, name='about')
                       #url(r'^lookup/', include('lookup.urls'))
    url(r'^lookup/', include('lookup.urls'))
)
