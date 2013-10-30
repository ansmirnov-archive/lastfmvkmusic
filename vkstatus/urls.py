from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'process_code/', views.process_code),
    url(r'send_last/', views.send_last),
#    url(r'iteration/', views.iteration),
)
