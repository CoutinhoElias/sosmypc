# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import resolve_url as r
#from __future__ import unicode_literals

from django.db import models


class Pessoa(models.Model):#<<<==== Testenado com 'django_tables2' no installed apps
    username = models.OneToOneField(User, blank=True, null=True, related_name='pessoa') #"%(class)s_related"
    nomepessoa = models.CharField('Nome', max_length=100, null=False, blank=False)
    sobrenomepessoa = models.CharField('Sobrenome', max_length=100, null=False, blank=False)
    cep = models.CharField('Cep', max_length=10, null=True, blank=False)
    tipologradouro = models.CharField('Tipo Logradouro', max_length=100, null=False, blank=False)
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.CharField('Número', max_length=10, null=False, blank=False)
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
#---------------------------------------------------------------------------------------------------------------------------------------


class Profissao(models.Model):# TA FEITO
    profissao = models.CharField(max_length=100,null=False, blank=False)


    class Meta:
        verbose_name_plural = 'profissões'
        verbose_name = 'profissão'


    def __str__(self):
        return self.profissao
#------------------------------------------------------------------------------------------------------------------------------------------


class ProfissoesPessoa(models.Model):
    pessoa = models.ForeignKey(Pessoa, related_name='profissoesPessoa')
    profissao = models.ForeignKey(Profissao)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=False, blank=False)


    class Meta:
        unique_together = ("pessoa", "profissao")
        verbose_name_plural = 'profissao da pessoa'
        verbose_name = 'profissão da pessoa'


    def __str__(self):
        return self.profissao.profissao #<<=== Profissao do class profissao equivalente ao nome da profissão
                   #self.profissao. <<=== Variavel deste class, equivalente ao id da profissao nesta tabela


    def nomepessoa(self):
        return self.pessoa.nomepessoa

    def get_absolute_url(self):
        return r('profissoes:detalhes_profissoes', pk=self.pk)
#------------------------------------------------------------------------------------------------------------------------------------------


class Qualificacao(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural= 'Qualificações'
        verbose_name = 'Qualificação'

    def __str__(self):
        return self.descricao
#------------------------------------------------------------------------------------------------------------------------------------------


class QualificacaoProfissoesPessoa(models.Model):# #Resolvido, não modificar
    profissao = models.ForeignKey(ProfissoesPessoa, related_name='qualificacaoProfissoesPessoa')
    qualificacao = models.ForeignKey(Qualificacao)


    class Meta:
        unique_together = ("profissao", "qualificacao")
        verbose_name_plural = 'qualificações das profissões da pessoa'
        verbose_name = 'qualificação da profissão da pessoa'


    def __str__(self):
        return self.qualificacao.descricao

    def __unicode__(self):
        return '%d: %s' % (self.profissao, self.qualificacao)
#------------------------------------------------------------------------------------------------------------------------------------------
#
# class Recipe(models.Model):
#     pub_date = models.DateTimeField('Date Published', auto_now_add = True)
#     title = models.CharField(max_length=200)
#     instructions = models.TextField()
#
# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(Recipe, related_name="ingredients")
#     ingredient = models.CharField(max_length=255)