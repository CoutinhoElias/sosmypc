"""sosmypc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from sosmypc.core import views
from sosmypc.core.views import geoCoordenada, pessoa_list, pessoa_detail

urlpatterns = [
    url(r'^$', 'sosmypc.core.views.home'),
    url(r'^registrotecnico/$', geoCoordenada, name='registrotecnico'),
    url(r'^admin/', admin.site.urls),
    url(r'^pessoas/$', pessoa_list),
    url(r'^pessoas/rest$', views.rest),
    url(r'^pessoas/(?P<pk>[0-9]+)/$', pessoa_detail),
]

# -----------------------------------------------------------
from rest_framework import routers
from sosmypc.core.views import PessoaViewSet

router = routers.DefaultRouter()
router.register(r'pessoas', PessoaViewSet)

urlpatterns = urlpatterns + [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]