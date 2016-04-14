from django.conf.urls import url, include

import sosmypc
from . import views
#---------------------------------------------------------------------------------------------------------------------------------------
urlpatterns = [

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),


    url(r'^pessoas/$', views.PessoaList.as_view()),
    url(r'^pessoas/(?P<pk>[0-9]+)/$', views.PessoaDetail.as_view()),


    url(r'^profissoespessoas/$', views.ProfissoesPessoaList.as_view()),
    url(r'^profissoespessoas/(?P<pk>[0-9]+)/$', views.ProfissoesPessoaDetail.as_view()),
]