from django.conf.urls import url

from sosmypc.financeiro.models import ContaPagar
from sosmypc.financeiro.models import ContaReceber
from . import views

urlpatterns = [
    url('^$', views.contas, name='contas'),
    url('^pagar/(?P<conta_id>\d+)/$', views.contas, {'classe': ContaPagar}, name='conta_a_pagar'),
    url('^receber/(?P<conta_id>\d+)/$', views.contas, {'classe': ContaReceber}, name='conta_a_receber'),
]

