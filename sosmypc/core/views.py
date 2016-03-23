import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from sosmypc.core.forms import CommentForm, LoginForm, RegistrationForm

from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from sosmypc.core.models import Pessoa, ProfissoesPessoa, QualificacaoProfissoesPessoa, Profissao
from sosmypc.core.serializers import PessoaSerializer


from django.shortcuts import render



from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

import urllib, json

# Create your views here.


from sosmypc.core.models import Pessoa#, Qualificacao, Tecnico

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
            qualificacoes = QualificacaoProfissoesPessoa.objects.filter(profissaopessoa=profissao)
            if qualificacoes.count() == 0:
                jsondata+='['
            for qualificacao in qualificacoes:
                jsondata+='"'+qualificacao.qualificacao.descricao+'",'
            jsondata=jsondata[:-1]+']},'
        jsondata =jsondata[:-1]+ ']},'

    jsondata = jsondata[:-1]+'\n]'
    return HttpResponse(jsondata,content_type='application/json')

#-----------------------------------------------------------------------------------------------------
def index_html(request):
    form = CommentForm()
    return render(request,'index.html',{'form':form})


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
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

#-----------------------------------------------------------------------------------------------------

# def login_html(request):
#     if request.method=='POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],password=cd['password'])
#             print ('Teste')
#             if user is not None:
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponse('Autenticação realizada com sucesso')
#                 else:
#                     return HttpResponse('Conta desabilitada')
#             else:
#                 return HttpResponse('Login ou senha inválidos')
#     else:
#         form = LoginForm()
#     #return render(request,'sosmypc/login.html',{'form':form})
#     return render(request,'sosmypc/login.html',{'form':form})


def lista(request):
    profissoes = Profissao.objects.all()
    return render(request,'sosmypc/professions_list.html',{'profissoes':profissoes})

@login_required
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

            return render(request, 'registration.html',
                          {
                              'form': RegistrationForm(),
                          })
        else:
            return render(request, 'registration.html',
                          {'form': form})



    else:
        form = RegistrationForm()
    #return render(request,'sosmypc/login.html',{'form':form})
    return render(request,'registration.html',{'form':form})


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


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#@csrf_exempt
@api_view(['GET','POST'])
def pessoa_list(request):
    """
    List all code pessoas, or create a new pessoa.
    """
    if request.method == 'GET':
        pessoas = Pessoa.objects.all()
        serializer = PessoaSerializer(pessoas, many=True)
        #return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PessoaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
def pessoa_detail(request, pk):
    """
    Retrieve, update or delete a code pessoa.
    """
    try:
        pessoa = Pessoa.objects.get(pk=pk)
    except Pessoa.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PessoaSerializer(pessoa)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PessoaSerializer(pessoa, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        pessoa.delete()
        return HttpResponse(status=204)


class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all().order_by('nomepessoa')
    serializer_class = PessoaSerializer
