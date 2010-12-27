from django.conf.urls.defaults import *

urlpatterns = patterns('academics.views',
    url('^reports/custom', 'custom_report', name='custom_report'),
    url('^student_report$', 'student_report', name='student_report'),
)
