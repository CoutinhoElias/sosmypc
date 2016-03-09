import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets

from sosmypc.core.forms import TecnicoForm

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from sosmypc.core.models import Pessoa
from sosmypc.core.serializers import PessoaSerializer

# Create your views here.


from sosmypc.core.models import Pessoa#, Qualificacao, Tecnico


def home(request):
    return render(request,'index.html')


def geoCoordenada(request):
    print(request.POST)
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        tipologradouro = request.POST['tipologradouro']
        logradouro = request.POST['logradouro']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        numero = request.POST['numero']
        estado = request.POST['estado']
        # longitude = request.POST['longitude']
        # latitude = request.POST['latitude']

        address = tipologradouro + ' ' + logradouro + ', ' + numero + ' - ' + bairro + ', ' + cidade + ' - ' + estado

        # address = "1600 Amphitheatre Parkway, Mountain View, CA"
        api_key = "AIzaSyBWKWlI1WE9nvuld9AVcpTZQItHLTUmWxo"
        api_response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

        if api_response_dict['status'] == 'OK':
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            print('Latitude:', latitude)
            print('Longitude:', longitude)

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)

            # cria uma pessoa
            pessoa = Pessoa.objects.create(username_id=user.pk,
                                      nomepessoa=user.get_full_name(),
                                      tipologradouro=tipologradouro,
                                      logradouro=logradouro,
                                      numero=numero,
                                      bairro=bairro,
                                      cidade=cidade,
                                      estado=estado,
                                      longitude=longitude,
                                      latitude=latitude)

            #Tecnico.objects.create(pessoa=pessoa, )  # insere o pk do pessoa.

            # )

            return render(request, 'registro_tecnico.html',
                          {
                              'latitude': latitude,
                              'longitude': longitude,
                              'form': TecnicoForm(),
                          })
        else:
            return render(request, 'registro_tecnico.html',
                          {'form': form})
    else:
        return render(request, 'registro_tecnico.html',
                      {'form': TecnicoForm()})


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
