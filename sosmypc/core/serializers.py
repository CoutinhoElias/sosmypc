# from rest_framework import serializers
# from sosmypc.core.models import *

# class PessoaSerializer(serializers.ModelSerializer):
#     #profissoesPessoa = serializers.StringRelatedField(many=True)
#     pessoa = serializers.StringRelatedField(many=True)
#
#     class Meta:
#         model = Pessoa
#         fields = ('id', 'nomepessoa', 'tipologradouro', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'longitude', 'latitude','pessoa')#,'profissoesPessoa'
#

#------------------------------------------------------------------------------------------------------------------------------------------
# class ProfissoesPessoaSerializer(serializers.ModelSerializer):
#     qualificacaoProfissoesPessoa = serializers.StringRelatedField(many=True)#Resolvido, não modificar
#
#     class Meta:
#         model = ProfissoesPessoa
#         fields = ('id', 'pessoa','profissao', 'rating','qualificacaoProfissoesPessoa')
#------------------------------------------------------------------------------------------------------------------------------------------

# class QualificacaoSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = QualificacaoProfissoesPessoa
#         fields = ('id','descricao')
#------------------------------------------------------------------------------------------------------------------------------------------

# class QualificacaoProfissoesPessoaSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = QualificacaoProfissoesPessoa
#         fields = ('id','profissaopessoa')

#------------------------------------------------------------------------------------------------------------------------------------------
# class ProfissaoSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profissao
#         fields = ('id', 'profissao')