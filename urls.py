from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import reporting
reporting.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^academics/', include('academics.urls')),
    (r'^reporting/', include('reporting.urls')),
    (r'^static/admin/(.*)', 'django.views.static.serve', {'document_root' : '/usr/share/pyshared/django/contrib/admin/media/', 'show_indexes' : True}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT, 'show_indexes':True}),
    (r'', include('home.urls')),
)
