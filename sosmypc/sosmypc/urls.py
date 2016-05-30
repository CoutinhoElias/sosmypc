
from django.conf.urls import url, include
from django.contrib import admin

from sosmypc.core import views
from django.contrib.auth.decorators import login_required

#from sosmypc.core.views import CreateQualificacao

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pessoas/rest$', views.rest),

    url(r'^$',views.index_html,name='sosmypc'),
    url('^', include('django.contrib.auth.urls')),
    #url(r'^profissoes/', include('sosmypc.core.urls', namespace="profissoes")),
    url(r'^site/', include('sosmypc.core.urls')),
    #url(r'^listaprofissoes/$', login_required(views.lista_profissoes)),


    url(r'^profissoespessoa/$', login_required(views.lista_profissoespessoa), name='profissoespessoa-list'),

    url(r'^cadastrar-profissao-pessoa/$', views.ProfissoesPessoaCreateView.as_view(), name='cadastrar-profissao-pessoa'),

    url(r'^cadastrarprofissaopessoa/$',views.pp,name='cadastrarprofissaopessoa'),
    #url(r'^cadastrar-profissao-pessoa/$', views.ProfissoesPessoa_View, name='cadastrar-profissao-pessoa'),

    # url(r'^qualificacao/add/$', CreateQualificacao.as_view(), name='add_qualificacao'),
    # url(r'^qualificacao/$', views.lista_qualificacao, name='qualificacao-list'),

    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^', include('sosmypc.core.api.urls')),

    url(r'^financeiro/', include('sosmypc.financeiro.urls')),
]
