from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'greenstreets.views.home', name='home'),
    # url(r'^greenstreets/', include('greenstreets.foo.urls')),

    # homepage
    url(r'^$', TemplateView.as_view(template_name='survey/index.html'), name='home'),
    
    # commuterform
    url(r'^commuterform/$', 'survey.views.commuter', name='commuterform'),

    # studentform
    url(r'^studentform/$', 'survey.views.student', name='studentform'),
    
    # schools
    url(r'^district/(?P<slug>[-\w]+)/schools/$', 'survey.views.get_schools'),
    
    (r'^grappelli/', include('grappelli.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
