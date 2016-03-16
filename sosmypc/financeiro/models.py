# -*- coding: utf-8 -*-
from django.db import models
from sosmypc.core.models import Pessoa
from django.utils.translation import ugettext_lazy as _

class Historico(models.Model):
    class Meta:
        ordering = ('descricao',)
    descricao = models.CharField(max_length=50)

    def __unicode__(self):
        return self.descricaos


CONTA_OPERACAO_DEBITO = 'd'
CONTA_OPERACAO_CREDITO = 'c'
CONTA_OPERACAO_CHOICES = (
    (CONTA_OPERACAO_DEBITO, _('Debito')),
    (CONTA_OPERACAO_CREDITO, _('Credito')),
)

CONTA_STATUS_APAGAR = 'a'
CONTA_STATUS_PAGO = 'p'
CONTA_STATUS_CHOICES = (
    (CONTA_STATUS_APAGAR, _('A Pagar')),
    (CONTA_STATUS_PAGO, _('Pago')),
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


class ContaPagar(Conta):
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_DEBITO
        super(ContaPagar, self).save(*args, **kwargs)

class ContaReceber(Conta):
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_CREDITO
        super(ContaReceber, self).save(*args, **kwargs)


class Pagamento(models.Model):
    class Meta:
        abstract = True

    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)

class PagamentoPago(Pagamento):
    conta = models.ForeignKey('ContaPagar')

class PagamentoRecebido(Pagamento):
    conta = models.ForeignKey('ContaReceber')