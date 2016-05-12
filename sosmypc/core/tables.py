# coding: utf-8
#import django_tables2 as tables

from .models import  Pessoa


# class CountryTable(tables.Table):
#     name = tables.Column()
#     population = tables.Column()
#     tz = tables.Column(verbose_name='time zone')
#     visits = tables.Column()
#     summary = tables.Column(order_by=("name", "population"))
#
#     class Meta:
#         model = Country
#
#
# class ThemedCountryTable(CountryTable):
#     class Meta:
#         attrs = {'class': 'paleblue'}
#
#
# class BootstrapTable(tables.Table):
#
#     country = tables.RelatedLinkColumn()
#
#     class Meta:
#         model = Person
#         template = 'django_tables2/bootstrap.html'


# class PessoaTable(tables.Table):
#     #username = tables.Column(verbose_name='BIFE_DO_OIAO')
#
#     class Meta:
#         model = Pessoa
#         # add class="paleblue" to <table> tag
#         attrs = {"class": "paleblue"}