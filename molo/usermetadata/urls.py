from molo.usermetadata import views

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^persona/$', views.PersonaView.as_view(), name='persona'),
)
