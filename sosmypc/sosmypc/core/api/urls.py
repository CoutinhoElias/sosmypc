from django.conf.urls import url, include

from . import views
#---------------------------------------------------------------------------------------------------------------------------------------


# router = DefaultRouter()
# router.register(r'pessoas1',  PessoaViewset)

urlpatterns = [

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    #url(r'^pessoas/$', views.PessoaList.as_view()),
    url(r'^pessoas/$', views.PessoaList.as_view()),
    url(r'^pessoas/(?P<pk>[0-9]+)/$', views.PessoaDetail.as_view()),
    # #Caminho mais curto para gerar rest
    # url(r'^pessoas1/$', pessoa_list, name='pessoas1'),
    # url(r'^pessoas1/(?P<pk>[0-9]+)/$', pessoa_detail, name='pessoa1'),
     #url(r'^pessoas1/', include(router.urls, namespace='pessoas1')),


    url(r'^profissoespessoas/$', views.ProfissoesPessoaList.as_view()),
    url(r'^profissoespessoas/(?P<pk>[0-9]+)/$', views.ProfissoesPessoaDetail.as_view()),

]