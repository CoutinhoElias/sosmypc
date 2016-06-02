import json
import urllib

import extra_views
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

#---
from material import *
from sosmypc import settings
from sosmypc.core.forms import CommentForm, RegistrationForm, ProfissoesPessoaForm, ProfissoesPessoaModelForm
from sosmypc.core.models import Pessoa
from sosmypc.core.models import ProfissoesPessoa, QualificacaoProfissoesPessoa, Profissao

from sosmypc.settings import LOGIN_URL
from django.shortcuts import resolve_url



def rest(request):
    pessoas = Pessoa.objects.all()

    jsondata = '['
    for pessoa in pessoas:
        jsondata += '\n{"nome":"'+pessoa.nomepessoa+'",' \
                    '\n  "endereco":"'+pessoa.tipologradouro+' '+pessoa.logradouro+', '+str(pessoa.numero)+'' \
                    '-'+pessoa.bairro+' '+pessoa.cidade+' - '+pessoa.estado+'",'
        jsondata += '\n  "coordenadas":"'+str(pessoa.latitude)+','+str(pessoa.longitude)+'",'
        jsondata += '\n  "profissoes":['
        profissoes = ProfissoesPessoa.objects.filter(pessoa=pessoa)
        if profissoes.count()==0:
            jsondata+='['
        for profissao in profissoes:
            jsondata+='\n  {"profissao":"'+profissao.profissao.profissao+'","rating":0,'
            jsondata+='\n   "qualificacoes":['
            qualificacoes = QualificacaoProfissoesPessoa.objects.filter(profissao=profissao)
            if qualificacoes.count() == 0:
                jsondata+='['
            for qualificacao in qualificacoes:
                jsondata+='"'+qualificacao.qualificacao.descricao+'",'
            jsondata=jsondata[:-1]+']},'
        jsondata =jsondata[:-1]+ ']},'

    jsondata = jsondata[:-1]+'\n]'
    return HttpResponse(jsondata,content_type='application/json')

#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para chamar página index
def index_html(request):
    form = CommentForm()
    return render(request,'index.html',{'form':form})

#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para chamar página dashboard
@login_required(login_url=LOGIN_URL)
def success(request):
    #form = CommentForm()
    return render(request,'dash.html')

#----------------------------------------------------------------------------------------------------------------------
#Funções utilizadas para Autenticação e validação quandonão se usar o Mixin.
def login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "sosmypc/login.html", {'redirect_to': next})


def Logout(request):
    return HttpResponseRedirect(settings.LOGIN_URL)


#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para listar todas as profissões cadastradas
@login_required(login_url=LOGIN_URL)
def lista_profissoes(request):
    profissoes = Profissao.objects.all()
    return render(request,'sosmypc/professions_list.html',{'profissoes':profissoes})

#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para listar profissões da pessoa que está logada
@login_required(login_url=LOGIN_URL)
def lista_profissoespessoa(request):
    #profissoespessoa = ProfissoesPessoa.objects.filter(pessoa__username=request.user)#<<<<====correto com filtro
    profissoespessoa = ProfissoesPessoa.objects.all()

    form_profissoespessoa = ProfissoesPessoaModelForm(initial={'pessoa': request.user.pessoa})

    return render(request,'sosmypc/person_and_professions_list.html',{'profissoespessoa':profissoespessoa, 'person_and_professions_list': form_profissoespessoa})

#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para inserir uma pessoa e user relacionados
def register_html(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Tratar os dados vindos do formulario de cadastro aqui
            cd = form.cleaned_data
            nome = cd['nome']
            splitname = nome.split()
            first_name = splitname[0] #Primeiro nome
            last_name = ' '.join(splitname[1:]) #Restante do nome

            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']
            cep = request.POST['cep']
            numero = request.POST['numero']
            logradouro = request.POST['logradouro']
            bairro = request.POST['bairro']
            cidade = request.POST['cidade']
            estado = request.POST['estado']

            address = logradouro+', '+str(numero)+' - '+bairro+', '+cidade+' - '+estado+', '+cep[:5]+'-'+cep[5:]
            latitude,longitude=geoCoordenada(address)

            if latitude!=None and longitude!=None:
                user = User.objects.create_user(username=username, email=email,
                                                password=password, first_name=first_name,
                                                last_name=last_name)

                # cria uma pessoa
                pessoa = Pessoa.objects.create(username_id=user.pk,
                                              nomepessoa=user.get_full_name(),
                                              cep=cep,       logradouro=logradouro,
                                              numero=numero, bairro=bairro,
                                              cidade=cidade, estado=estado,
                                              longitude=longitude,latitude=latitude)

            return  HttpResponseRedirect(resolve_url('dashboard'))
            # return render(request, 'registration.html',
            #               {
            #                   'form': RegistrationForm(),
            #               })
        else:
            return render(request, 'registration.html',
                          {'form': form})
    else:
        form = RegistrationForm()
    return render(request,'registration.html',{'form':form})


#----------------------------------------------------------------------------------------------------------------------
#Função utilizada para recuperar coordenadas geográficas do google
def geoCoordenada(endereco):
    address=endereco.replace(' ','+')
    api_key = getattr(settings, "API_MAPS", None)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(urllib.parse.quote(address), api_key)
    response = urllib.request.urlopen(url).read().decode('utf8')
    result = json.loads(response)
    latitude = None
    longitude= None
    if result['status'] == 'OK':
        latitude = result['results'][0]['geometry']['location']['lat']
        longitude = result['results'][0]['geometry']['location']['lng']
    else:
        latitude = longitude = 0
    return latitude,longitude


#-----------------------------------------------------------------------------------------------------------------------
class ItemInline(extra_views.InlineFormSet):
    model = QualificacaoProfissoesPessoa
    fields = ['id', 'qualificacao']
    extra = 1# Define aquantidade de linhas a apresentar.



#LoginRequiredMixin faz a mesma função de @login_required(login_url=LOGIN_URL). a ndiferença que LoginRequiredMixin não precisa apontar na url
class NewProfissoesPessoaView(LoginRequiredMixin,LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.CreateWithInlinesView):
    title = "Nova Profissão"
    model = ProfissoesPessoa

    #print('Chegou na linha 334')

    layout = Layout(
        Row('profissao', 'rating'),
        Inline('Qualificações da Profissão', ItemInline),
    )
    #print('Chegou na linha 340')

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)
        self.object.pessoa_id = self.request.user.id
        self.object.save()
        return super(NewProfissoesPessoaView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()


class UpdateProfissoesPessoaView(LoginRequiredMixin,LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.UpdateWithInlinesView):
    title = "Atualizando Profissões"
    model = ProfissoesPessoa
    layout = Layout(
        Row('profissao', 'rating'),

        Inline('Qualificações da Profissão', ItemInline),
    )

    def get_success_url(self):
        return self.object.get_absolute_url()

#-------------------------------------------------------------------------------------------------------
#Função utilizada para inserir uma pessoa e user relacionados
def funcaoProfissoesPessoa(request):
    if request.method=='POST':
        form = ProfissoesPessoaForm(request.POST)
        if form.is_valid():

            # pessoa = request.POST['pessoa']
            # profissao = request.POST['profissao']
            # rating = request.POST['rating']

            # form.cleaned_data['pessoa']
            # form.cleaned_data['profissao']
            # form.cleaned_data['rating']

            ProfissoesPessoa.objects.create(form.cleaned_data['pessoa'],
                                            form.cleaned_data['profissao'],
                                            form.cleaned_data['rating'])

            return render(request, 'sosmypc/profissoes_pessoa_forms.html',
                          {
                              'form': ProfissoesPessoaForm(),
                          })
            print('Se form for valido<<<=======================')
            # return HttpResponseRedirect('/cadastrarprofissaopessoa/')

        else:
            return render(request, 'sosmypc/profissoes_pessoa_forms.html', {'profissao_pessoa_modal_form':form})
            print('Se form for invalido<<<=======================')
    else:
        form = ProfissoesPessoaForm()
        return render(request, 'sosmypc/profissoes_pessoa_forms.html', {'profissao_pessoa_modal_forms':form})
        print('Se o metodo não for POST<<<=======================')


def pp(request):
    if request.method == 'POST':
        form = ProfissoesPessoaModelForm(request.POST)

        if not form.is_valid():
            return render(request, 'sosmypc/profissoes_pessoa_forms.html', {'form':form})

        pessoa = form.cleaned_data.get('pessoa')
        profissao = form.cleaned_data.get('profissao')
        rating = form.cleaned_data.get('rating')

        ProfissoesPessoa.objects.create(pessoa=pessoa,
                                        profissao=profissao,
                                        rating=rating)


        return HttpResponseRedirect('/cadastrarprofissaopessoa/')
    else:
        return render(request, 'sosmypc/profissoes_pessoa_forms.html', {'form':ProfissoesPessoaModelForm(initial={'pessoa': request.user.pessoa})})


# usei BaseCreateView porque estava com preguica de fazer um template para renderizar essa view, ou seja, essa sera uma view so de processamento
# vc vai poder fazer um post para ela.
# class ProfissoesPessoaCreateView(generic.CreateView):

class ProfissoesPessoaCreateView(generic.CreateView):
    model = ProfissoesPessoa
    form_class = ProfissoesPessoaModelForm
    success_url = reverse_lazy('profissoespessoa-list')