# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from __future__ import unicode_literals
from sosmypc.core.static.material.frontend import Module


class Sample(Module):
    icon = 'mdi-image-compare'


class Pessoa(models.Model):# TA FEITO
    username = models.OneToOneField(User, blank=True, null=True)
    nomepessoa = models.CharField('Nome', max_length=100, null=False, blank=False)
    sobrenomepessoa = models.CharField('Sobrenome', max_length=100, null=False, blank=False)
    tipologradouro = models.CharField('Tipo Logradouro', max_length=100, null=False, blank=False)
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.IntegerField('Número', null=False, blank=False)
    bairro = models.CharField('Bairro', max_length=50, null=False, blank=False)
    cidade = models.CharField('Cidade', max_length=50, null=False, blank=False)
    estado = models.CharField('estado', max_length=10, null=False, blank=False)
    longitude = models.FloatField('Longitude', null=True, blank=True)
    latitude = models.FloatField('Latitude', null=True, blank=True)


    class Meta:
        verbose_name_plural = 'pessoas'
        verbose_name = 'pessoa'


    def __str__(self):
        return self.nomepessoa


#------------------------------------------------------------------------------------------------------------------------------------------
class Profissao(models.Model):# TA FEITO
    profissao = models.CharField(max_length=100,null=False, blank=False)


    class Meta:
        verbose_name_plural = 'profissões'
        verbose_name = 'profissão'


    def __str__(self):
        return self.profissao


#------------------------------------------------------------------------------------------------------------------------------------------
class ProfissoesPessoa(models.Model):# MANY_TO_MANY MANUAL
    pessoa = models.ForeignKey(Pessoa, related_name='profissoesPessoa')
    profissao = models.ForeignKey(Profissao)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False, blank=False)


    class Meta:
        unique_together = ("pessoa", "profissao")
        verbose_name_plural = 'profissao da pessoa'
        verbose_name = 'profissão da pessoa'


    def __unicode__(self):
        return "%s is in profissao %s (as %s)" % (self.pessoa, self.profissao, self.type) # <<=== Ambas são Variáveis local deste class



    def __str__(self):
        return self.profissao.profissao #<<=== Profissao do class profissao equivalente ao nome da profissão
                   #self.profissao. <<=== Variavel deste class, equivalente ao id da profissao nesta tabela


    def nomepessoa(self):
        return self.pessoa.nomepessoa


#------------------------------------------------------------------------------------------------------------------------------------------

class Qualificacao(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural= 'Qualificações'
        verbose_name = 'Qualificação'

    def __str__(self):
        return self.descricao

#------------------------------------------------------------------------------------------------------------------------------------------

class QualificacaoProfissoesPessoa(models.Model):# MANY_TO_MANY MANUAL
    profissaopessoa = models.ForeignKey(ProfissoesPessoa, related_name='qualificacaoProfissoesPessoa')
    qualificacao = models.ForeignKey(Qualificacao)


    class Meta:
        unique_together = ("profissaopessoa", "qualificacao")
        verbose_name_plural = 'qualificações das profissões da pessoa'
        verbose_name = 'qualificação da profissão da pessoa'



    #def nomepessoa(self):
    #    return self.qualificacao.descricao

#------------------------------------------------------------------------------------------------------------------------------------------
"""class Comentarios(models.Model):# TA FEITO
    profissaopessoa = models.ForeignKey(ProfissoesPessoa)
    comentario = models.TextField(max_length=200,null=False, blank=False)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False, blank=False)



    class Meta:
        #unique_together = ("pessoa", "profissao")
        verbose_name_plural = 'comentários dos profissionais'
        verbose_name = 'comentários do profissional'

    def nomepessoa(self):
        return self.profissaopessoa.pessoa.nomepessoa"""


