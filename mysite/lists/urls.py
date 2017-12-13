from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^new$', new_list, name='new_list'),
    url(r'^(?P<pk>\d+)/$', view_list, name='view_list'),
    url(r'^(?P<pk>\d+)/add_item$', add_item, name='add_item'),
]
