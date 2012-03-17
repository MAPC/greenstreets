from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # homepage
    url(r'^$', direct_to_template, {'template': 'survey/index.html'}, name='home'),
    
    # commuterform
    url(r'^commuterform/$', 'survey.views.commuter', name='commuterform'),

    # studentform
    url(r'^studentform/$', 'survey.views.student', name='studentform'),
    
    # get data
    url(r'^district/(?P<slug>[-\w]+)/schools/$', 'survey.views.get_schools'),
)


