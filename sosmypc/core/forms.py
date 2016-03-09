from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(forms.Form):
    username = forms.CharField(label="Nome usuário", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))
    #password = forms.CharField(label="Senha", max_length=32, widget=forms.PasswordInput(
        #attrs={'class': 'form-control input-lg'}))
    first_name = forms.CharField(label="Primeiro nome", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))
    last_name = forms.CharField(label="Sobrenome", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control input-lg'}))
    is_staff = forms.BooleanField(label="É usuário do sistema?", initial=False)
    is_superuser = forms.BooleanField(label="É Administrador do sistema?", initial=False)
    email = forms.EmailField(max_length=32, widget=forms.EmailInput(
        attrs={'class': 'form-control input-lg'}))



class TecnicoForm(forms.Form, UserCreationForm):
    #username = forms.CharField(label="Nome de usuário", max_length=32, widget=forms.TextInput(
    #    attrs={'placeholder': 'Nome de usuário', 'class': 'form-control input-lg'}))

    #password = forms.CharField(label="Senha", max_length=32, widget=forms.PasswordInput(
    #    attrs={'placeholder': 'Sua senha', 'class': 'form-control input-lg'}))

    first_name = forms.CharField(label="Primeiro nome", max_length=32, widget=forms.TextInput(
        attrs={'placeholder': 'Primeiro nome','class': 'form-control input-lg'}))

    last_name = forms.CharField(label="Restante do nome", max_length=32, widget=forms.TextInput(
        attrs={'placeholder': 'Restante do seu nome','class': 'form-control input-lg'}))

    email = forms.EmailField(max_length=32, widget=forms.EmailInput(
        attrs={'placeholder': 'E-Mail de usuário','class': 'form-control input-lg'}))


    #sobrenome = forms.CharField(label="Sobrenome", required=False, widget=forms.TextInput(
    #    attrs={'placeholder': 'Sobrenome', 'class': 'form-control'}))

    tipologradouro = forms.CharField(label="Tipo Logradouro", widget=forms.TextInput(
        attrs={'placeholder': 'Tipo Logradouro', 'class': 'form-control'}))

    logradouro = forms.CharField(label="Logradouro", widget=forms.TextInput(
        attrs={'placeholder': 'Logradouro', 'class': 'form-control'}))

    numero = forms.CharField(label="Número", widget=forms.TextInput(
        attrs={'placeholder': 'Número', 'class': 'form-control'}))

    bairro = forms.CharField(label="Bairro", widget=forms.TextInput(
        attrs={'placeholder': 'Bairro', 'class': 'form-control'}))

    cidade = forms.CharField(label="Cidade", widget=forms.TextInput(
        attrs={'placeholder': 'Cidade', 'class': 'form-control'}))

    estado = forms.CharField(label="Estado", widget=forms.TextInput(
        attrs={'placeholder': 'Estado', 'class': 'form-control'}))
    # latitude = forms.CharField(label="Latitude")
    # longitude = forms.CharField(label="Longitude")


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