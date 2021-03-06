"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from myapp.views import HelloWord, products, product_detail, product_create, product_edit, product_delete
from loginapp.views import login, logout


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HelloWord.as_view()),

    url(r'^products/$', products, name='products'),
    url(r'^products/(?P<id>\d+)/$', product_detail, name='product_detail'),
    url(r'^products/new/$', product_create, name='product_create'),
    url(r'^products/(?P<id>\d+)/edit/$', product_edit, name='product_edit'),
    url(r'^products/(?P<id>\d+)/delete/$', product_delete, name='product_delete'),

    url(r'^login/$', login),
    url(r'^logout/$', logout),

    # hello CBV.
    url(r'^unions/', include('unionapp.urls', namespace='unionapp')),
    url(r'^api/', include('api.urls')),

    # scrapers
    url(r'^scrapers/', include('scrapers.urls', namespace='scrapers')),

    url(r'^lists/', include('lists.urls', namespace='lists')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
