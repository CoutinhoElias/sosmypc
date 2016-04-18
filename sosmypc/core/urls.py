from django.views import generic
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from sosmypc.core import forms
from . import views


urls_profissoes =[
     url(r'^$', views.NewProfissoesPessoaView.as_view(template_name="person_and_professions.html")),
     url(r'^(?P<pk>\d+)/$', views.UpdateProfissoesPessoaView.as_view(), name='detalhes_profissoes'),
]

urlpatterns = [
    url(r'^$',views.index_html,name='sosmypc'),
    #url(r'^login/$',views.login,name='login'),--
    url(r'^registro/$',views.register_html,name='registro'),
    #url('^profissoes/$', views.NewProfissoesPessoaView.as_view(template_name="person_and_professions.html"),name="profissoes"),
    url(r'^profissoes/', include(urls_profissoes,namespace="profissoes")),
]
