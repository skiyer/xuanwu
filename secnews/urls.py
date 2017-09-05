from django.conf.urls import url

from . import views

app_name = 'secnews'
urlpatterns = [
    # ex: /secnews/
    url(r'^$', views.index, name='index'),
    # ex: /secnews/2017/01/01/
    url(r'^(?P<y>[0-9]+)/(?P<m>[0-9]+)/(?P<d>[0-9]+)/$', views.date_view, name='date_view'),
    # ex: /secnews/search
    url(r'^search$', views.search, name='search'),
]