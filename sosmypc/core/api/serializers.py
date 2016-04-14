from django.contrib.auth.models import User
from rest_framework import serializers


from sosmypc.core.models import Pessoa, Profissao, ProfissoesPessoa


class UserSerializer(serializers.ModelSerializer):
    pessoa = serializers.StringRelatedField()#Resolvido, não modificar Obs: Só pode ser many=True se tiver relacionado User com Pessoa

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'pessoa')


class PessoaSerializer(serializers.ModelSerializer):
    profissoesPessoa = serializers.StringRelatedField(many=True)#Resolvido, não modificar

    class Meta:
        model = Pessoa
        fields = ('id',
                  'username',
                  'nomepessoa',
                  'sobrenomepessoa',
                  'cep',
                  'tipologradouro',
                  'logradouro',
                  'numero',
                  'bairro',
                  'cidade',
                  'estado',
                  'estado',
                  'profissoesPessoa')


class ProfissoesPessoaSerializer(serializers.ModelSerializer):
    qualificacaoProfissoesPessoa = serializers.StringRelatedField(many=True)#Resolvido, não modificar

    class Meta:
        model = ProfissoesPessoa
        fields = ('id',
                  'pessoa',
                  'profissao',
                  'rating',
                  'qualificacaoProfissoesPessoa')

class QualificacaoProfissoesPessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfissoesPessoa
        fields = ('id',
                  'profissao',
                  'qualificacao')
