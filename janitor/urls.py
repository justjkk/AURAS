from django.conf.urls.defaults import *

urlpatterns = patterns('janitor.views',
    url('^bulk_upload$', 'bulk_upload', name='bulk_upload'),
    url('^bulk_upload/(?P<status>success)$', 'bulk_upload'),
)
