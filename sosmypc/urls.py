
from django.conf.urls import url, include
from django.contrib import admin

from sosmypc.core import views
from django.contrib.auth.decorators import login_required

from sosmypc.core.views import CreateMyModelView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^pessoas/rest$', views.rest),

    url(r'^$',views.index_html,name='sosmypc'),
    url('^', include('django.contrib.auth.urls')),
    #url(r'^profissoes/', include('sosmypc.core.urls', namespace="profissoes")),
    url(r'^site/', include('sosmypc.core.urls')),
    #url(r'^listaprofissoes/$', login_required(views.lista_profissoes)),
    url(r'^profissoespessoa/$', login_required(views.lista_profissoespessoa)),

    url(r'^create/', CreateMyModelView.as_view(), name='create_mymodel_form'),
    #url(r'^congratulations/', TemplateView.as_view(template_name="myapp/create_mymodel_success.html"), name='create_mymodel_success'),


    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^', include('sosmypc.core.api.urls')),

    url(r'^financeiro/', include('sosmypc.financeiro.urls')),
]
