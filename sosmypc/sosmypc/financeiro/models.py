# -*- coding: utf-8 -*-
from django.db import models
from sosmypc.core.models import Pessoa
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class HistoricoManager(models.Manager):#Criando meu Manager personalizado
    def get_queryset(self):
        queryset = super(HistoricoManager, self).get_queryset()

        return queryset.extra(
            select = {
                '_valor_total': """select sum(valor) from financeiro_conta
                                  where financeiro_conta.historico_id = financeiro_historico.id""",
                }
            )

class Historico(models.Model):
    class Meta:
        ordering = ('descricao',)
    descricao = models.CharField(max_length=50)

    objects = HistoricoManager()

    def valor_total(self):
        return self._valor_total or 0.0

    def __str__(self):
        return self.descricao


CONTA_OPERACAO_DEBITO = 'd'
CONTA_OPERACAO_CREDITO = 'c'
CONTA_OPERACAO_CHOICES = (
    (CONTA_OPERACAO_DEBITO, _('Debito')),
    (CONTA_OPERACAO_CREDITO, _('Credito')),
)

CONTA_STATUS_APAGAR = 'a'
CONTA_STATUS_PAGO = 'p'
CONTA_STATUS_CHOICES = (
    (CONTA_STATUS_APAGAR, _('Aberta')),
    (CONTA_STATUS_PAGO, _('Paga')),
)

class Conta(models.Model):
    class Meta:
        ordering = ('-data_vencimento', 'valor')

    pessoa = models.ForeignKey(to='core.Pessoa')
    historico = models.ForeignKey('Historico')
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    operacao = models.CharField(
        max_length=1,
        default=CONTA_OPERACAO_DEBITO,
        choices=CONTA_OPERACAO_CHOICES,
        blank=True,
        )
    status = models.CharField(
        max_length=1,
        default=CONTA_STATUS_APAGAR,
        choices=CONTA_STATUS_CHOICES,
        blank=True,
        )
    descricao = models.TextField(blank=True)

    def __unicode__(self):
        data_vencto = self.data_vencimento.strftime('%d/%m/%Y')
        valor = '%0.02f'%self.valor
        return '%s - %s (%s)'%(valor, self.pessoa.nome, data_vencto)


class ContaPagar(Conta):
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_DEBITO
        super(ContaPagar, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural= 'Contas a Pagar'
        verbose_name = 'Conta a Pagar'

    def get_absolute_url(self):
        return reverse('conta_a_pagar', kwargs={'conta_id': self.id})

class ContaReceber(Conta):
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_CREDITO
        super(ContaReceber, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural= 'Contas a Receber'
        verbose_name = 'Conta a Receber'

    def get_absolute_url(self):
        return reverse('conta_a_receber', kwargs={'conta_id': self.id})


class Pagamento(models.Model):
    class Meta:
        abstract = True

    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)

class PagamentoPago(Pagamento):
    conta = models.ForeignKey('ContaPagar')

class PagamentoRecebido(Pagamento):
    conta = models.ForeignKey('ContaReceber')