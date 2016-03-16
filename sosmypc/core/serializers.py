from rest_framework import serializers
from sosmypc.core.models import *



"""class QualificacoesSerializer(serializers.ModelSerializer): #QualificacaoSerializer

    #qualificacoes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Qualificacao
        fields = ('id','descricao')
"""

#------------------------------------------------------------------------------------------------------------------------------------------
class QualificacoesProfissoesPessoaSerializer(serializers.ModelSerializer): #QualificacaoSerializer

    #qualificacoesProfissoesPessoa = serializers.StringRelatedField(many=True)

    class Meta:
        model = QualificacaoProfissoesPessoa
        fields = ('id','profissaopessoa')


#------------------------------------------------------------------------------------------------------------------------------------------
class ProfissoesPessoaSerializer(serializers.ModelSerializer): #ProfissaoSerializer
    #qualificacaoProfissaoPessoa = QualificacoesProfissoesPessoaSerializer(many=True)
    qualificacaoProfissaoPessoa = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProfissoesPessoa
        fields = ('id', 'profissao', 'rating','qualificacaoProfissaoPessoa')

#------------------------------------------------------------------------------------------------------------------------------------------

class PessoaSerializer(serializers.ModelSerializer):
    #profissaoPessoa = ProfissoesPessoaSerializer(many=True)
    profissaoPessoa = serializers.StringRelatedField(many=True)

    class Meta:
        model = Pessoa
        fields = ('id', 'nomepessoa', 'tipologradouro', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'longitude', 'latitude','profissaoPessoa')


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Pessoa.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        #instance.nomepessoa = validated_data.get('nomepessoa', instance.title)
        #instance.sobrenomepessoa = validated_data.get('sobrenomepessoa', instance.code)
        #instance.tipologradouro = validated_data.get('tipologradouro', instance.linenos)
        #instance.logradouro = validated_data.get('logradouro', instance.language)
        #instance.numero = validated_data.get('numero', instance.style)
        #instance.bairro = validated_data.get('bairro', instance.style)
        #instance.cidade = validated_data.get('cidade', instance.style)
        #instance.estado = validated_data.get('estado', instance.style)
        #instance.longitude = validated_data.get('longitude', instance.style)
        #instance.latitude = validated_data.get('latitude', instance.style)

        #instance.save()
        #return instance