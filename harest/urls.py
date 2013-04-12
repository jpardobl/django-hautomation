from django.conf.urls import patterns, include, url


urlpatterns = patterns('harest',
    url(r'^manage/device/(?P<did>[\d\w]+)', 'views_device.entrance', name='device_by_id'),
    url(r'^manage/device/', 'views_device.entrance', name='device'),

    url(r'^cmd/pl_switch/(?P<protocol>[a-z0-9A-Z]{3,4})/(?P<did>[\d\w]+)/?', 'views_cmds.pl_switch', name="pl_switch"),
)
