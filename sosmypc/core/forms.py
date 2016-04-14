from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from material import Layout, Row, Fieldset, Span3, Span2, Span10, Span8, Span7, Span5
from django.forms.models import inlineformset_factory

from sosmypc.core.models import ProfissoesPessoa
from sosmypc.core.models import QualificacaoProfissoesPessoa


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,label="Nome")
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput,label="Senha")

class RegistrationForm(forms.Form, UserCreationForm):
    username = forms.CharField(max_length=30,required=True,label='Login')
    email = forms.EmailField(label="E-mail",required=True)
    #senha = forms.CharField(widget=forms.PasswordInput,label='Senha')
    #confirma_senha = forms.CharField(widget=forms.PasswordInput, label="Confirmar senha")

    nome = forms.CharField(required=True,label='Nome Completo')
    cep  = forms.IntegerField(max_value=99999999,required=True,label='CEP')
    #tipo_logradouro = forms.CharField(required=True,label='Tipo')
    logradouro = forms.CharField(required=True,label='Logradouro')
    numero = forms.CharField(required=True,label='Número')
    bairro = forms.CharField(required=True,label='Bairro')
    cidade = forms.CharField(required=True,label='Cidade')
    estado = forms.CharField(required=True,label='UF')

    #last_name = forms.CharField(required=True, label='Último nome')
    #gender = forms.ChoiceField(choices=((None, ''), ('F', 'Feminino'), ('M', 'Masculino'), ('O', 'Outro')),label='Gênero',required=False)
    profissional = forms.BooleanField(required=False, label='Sou profissional')
    agree_toc = forms.BooleanField(required=True, label='Eu aceito os termos e condições de uso.')

    layout = Layout(
                 Fieldset('Cadastrar em SOS my PC',
                    'username','email',
                    Row('password1', 'password2')),
                 Fieldset('Dados Pessoais','nome',
                    Row(Span2('cep'),# Span2('tipo_logradouro'),
                    Span8('logradouro'),Span2('numero')),
                    Row(Span5('bairro'),Span5('cidade'),Span2('estado'))  ),
                             'profissional', 'agree_toc')


class CommentForm(forms.Form):
    nome = forms.CharField(required=True,label='Nome Completo')
    email=forms.EmailField(label="E-mail",required=True)
    mensagem=forms.CharField(required=True,label='Comentário',widget=forms.Textarea)


class UserForm(forms.Form):
    username = forms.CharField(label="Nome usuário", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))

    email = forms.EmailField(max_length=32, widget=forms.EmailInput(
        attrs={'class': 'form-control input-lg'}))

    #password = forms.CharField(label="Senha", max_length=32, widget=forms.PasswordInput(
        #attrs={'class': 'form-control input-lg'}))
    first_name = forms.CharField(label="Primeiro nome", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))
    last_name = forms.CharField(label="Sobrenome", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))
    is_staff = forms.BooleanField(label="É usuário do sistema?", initial=False)
    is_superuser = forms.BooleanField(label="É Administrador do sistema?", initial=False)

class ProfissaoForm(forms.Form):
    profissao = forms.CharField(max_length=30,label="Profissao")

class ProfissoesPessoaForm(forms.ModelForm):  #<<=== Utiliza o forms desta maneira para lidar com inline no template.
        class Meta:
            model = ProfissoesPessoa
            fields = '__all__'


class QualificacaoProfissoesPessoaForm(forms.ModelForm):
        class Meta:
            model = QualificacaoProfissoesPessoa
            fields = '__all__'

        exclude = ['profissao']

# Para fazer inlineformset_factory  nos templates personalizados devemos criar os forms que vamos trabalhar.
# Tente colocar na ordem, isso não importa mas fica legível para outro programador.
# No exemplo criamos ProfissoesPessoaForm e QualificacaoProfissoesPessoaForm
# Em seguida os importamos no topo desta página.
# Enfim definimos o inlineformset_factory na linha acima destes comentáros.

#
# MAX_INGREDIENTS = 3
#
# IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, fields='__all__', can_delete=False, extra=MAX_INGREDIENTS)
#
# class UserSubmittedRecipeForm(forms.ModelForm):
#     class Meta:
#         model = Recipe
#         exclude = ('pub_date', )



"""Passos para trabalhar com django rest

1 - pip install djangorestframework
2 - pip instal httpie
3 - No Setting do projeto antes de suas apps insira 'rest_framework',
4 - No urls.py chame assim:
    url(r'^pessoas/all/', all_pessoas)

5 - Na pasta do projeto (Neste caso a pasta core onde se encontram os arquivos views, forms, apps e models.py
    vamos criar um arquivo chamado serializers.py

    Neste arquivo vamos colocar o código abaixo:

    from rest_framework import serializers
    from core.models import *

    class PessoaSerializer(serializes. ModelSerializer):
        class Meta:
            model = Pessoa
            fields = ('pk', ...)

    Repita isso para cada classe do models.py

6 - Na views.py vamos fazer os seguintes passos:

    from django.shortcuts import render
    from django.views.decorators.csrf import csrf_exempt

    from rest_framework.renderes import JSONRenderer
    from rest_framework.renderes import Response
    from rest_framework.decorators import api_view

    from Pessoa.serializers import *

    @api_view(['GET'])
    def all_Pessoas(request, **kwargs):
        pessoas = Pessoa.objects.all()

        serializers = PessoaSerializer(pessoas, many=True)
            return Response(serializers.data)
"""
