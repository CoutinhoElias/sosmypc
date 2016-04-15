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
from django.conf import settings
from sosmypc.core import views, urls
from sosmypc.core.views import geoCoordenada#, pessoa_list, pessoa_detail
from django.contrib.auth.decorators import login_required
#from material.frontend import urls as frontend_urls

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import views as auth_views
# from sosmypc.financeiro.views import lista, json_contas


urlpatterns = [
    #url(r'', include(frontend_urls)),--
    url(r'^admin/', admin.site.urls),
    #url(r'^pessoas/$', pessoa_list),
    url(r'^pessoas/rest$', views.rest),
    #url(r'^pessoas/(?P<pk>[0-9]+)/$', pessoa_detail),

    url(r'^$',views.index_html,name='sosmypc'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^site/', include('sosmypc.core.urls')),
    url(r'^listaprofissoes/$', login_required(views.lista_profissoes)),
    url(r'^profissoespessoa/$', login_required(views.lista_profissoespessoa)),

    #url(r'^ppp/$', login_required(views.profissoesPessoa)),
    #url(r'^aqui$', login_required(views.profissoesPessoa), name='profissao-pessoa'),# Deu certo.


    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^', include('sosmypc.core.api.urls')),

    url(r'^financeiro/', include('sosmypc.financeiro.urls')),

    # url(r'^pessoas/lista/$', lista, name='pessoas_lista'),
    # url(r'^json/contas/(?P<id_pessoa>[0-9]+)/$', json_contas, name='json_contas'),


]
# -----------------------------------------------------------
