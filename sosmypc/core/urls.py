from django.views import generic
from django.conf.urls import url, include

from sosmypc.core import forms
from . import views


urlpatterns = [
   url(r'^$',views.index_html,name='sosmypc'),
   #url(r'^login/$',views.login,name='login'),--
   url(r'^registro/$',views.register_html,name='registro'),
   url('^profissoes/$', views.NewProfissoesPessoaView.as_view(template_name="person_and_professions.html"),
        name="profissoes_new"),
]
