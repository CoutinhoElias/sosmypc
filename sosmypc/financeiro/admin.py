from django.contrib import admin
from django.contrib.admin.options import ModelAdmin, TabularInline
from sosmypc.core.models import Pessoa
from sosmypc.financeiro.models import Historico, Conta, ContaPagar, ContaReceber, PagamentoPago, PagamentoRecebido


class AdminHistorico(ModelAdmin):
    list_display = ('descricao',)


class AdminConta(ModelAdmin):
    list_display = ('data_vencimento', 'valor', 'status', 'operacao', 'historico', 'pessoa',)
    search_fields = ('descricao',)
    list_filter = ('data_vencimento', 'status', 'operacao', 'historico', 'pessoa',)


class InlinePagamentoPago(TabularInline):
    model = PagamentoPago


class AdminContaPagar(ModelAdmin):
    list_display = ('data_vencimento','valor','status','historico','pessoa')
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao',]
    inlines = [InlinePagamentoPago,]
    date_hierarchy = 'data_vencimento'


class InlinePagamentoRecebido(TabularInline):
    model = PagamentoRecebido

class AdminContaReceber(ModelAdmin):
    list_display = ('data_vencimento','valor','status','historico','pessoa')
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao',]
    inlines = [InlinePagamentoRecebido,]
    date_hierarchy = 'data_vencimento'


admin.site.register(Historico, AdminHistorico)
admin.site.register(Conta, AdminConta)
admin.site.register(ContaPagar, AdminContaPagar)
admin.site.register(ContaReceber, AdminContaReceber)