from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url('^$', views.landing_page, name='ecosystem.landing_page'),
    url('^tutorial/(?P<page>\w+)?$', views.tutorial_page, name='ecosystem.tutorial_page'),
)
