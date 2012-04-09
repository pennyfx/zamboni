from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url('^$', views.landing_page, name='ecosystem.landing_page'),
    url('^sub/', views.content_page, name='ecosystem.content_page'),
)
