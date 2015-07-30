"""
urls.py - Django URL mappings
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^users/(?P<email>.*)/$', views.get_user, name='get_user'),
    url(r'^users$', views.add_user, name='add_user'),
    url(r'^news/(?P<news_type>.*)$', views.get_news, name='get_news'),
]

