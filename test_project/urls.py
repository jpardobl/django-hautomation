from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^rest/', include('harest.urls')),

)
