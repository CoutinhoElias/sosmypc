import extra_views
import json
import urllib

from django.template.loader import render_to_string
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from material import LayoutMixin, Layout, Inline, Row
#---
from sosmypc import settings
from sosmypc.core.forms import CommentForm, RegistrationForm
from sosmypc.core.models import Pessoa
from sosmypc.core.models import ProfissoesPessoa, QualificacaoProfissoesPessoa, Profissao
from sosmypc.settings import LOGIN_URL
from django.shortcuts import resolve_url

#from .tables  import PessoaTable

from django.views.generic import TemplateView
#from django_tables2 import RequestConfig
# Your write the four classes imported below
# (and pick a better location)

#from django_tables2 import SingleTableView


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
    logout(request)
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

    return render(request,'sosmypc/person_and_professions_list.html',{'profissoespessoa':profissoespessoa})
#----------------------------------------------------------------------------------------------------------------------
#Profissoes list Teste para uso em Modal
class CreateMyModelView(CreateView):
    model = ProfissoesPessoa
    template_name = 'sosmypc/person_and_professions_list.html'
    #success_url = reverse_lazy("create_mymodel_success")
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
    title = "Nova Profissão"
    model = ProfissoesPessoa
    layout = Layout(
        Row('profissao', 'rating'),

        Inline('Qualificações da Profissão', ItemInline),
    )

    def get_success_url(self):
        return self.object.get_absolute_url()


#----------------------------------------------------------------------------------------------------------------
def people(request): #<<<=== Vai listar informações de pessoas
    table = PessoaTable(Pessoa.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "sosmypc/people.html", {"people": Pessoa.objects.all()})
    #return render(request, "sosmypc/people.html", {"people": Pessoa.objects.filter(username=request.user)})<<<====Opção para usar filtro de usuario


    # profissoespessoa = ProfissoesPessoa.objects.filter(pessoa__username=request.user)
    #
    # return render(request,'sosmypc/people.html',{'profissoespessoa':profissoespessoa})
#
#
# class FooTableView(TemplateView):
#     template_name = 'app/foo_table.html'
#
#     def get_queryset(self, **kwargs):
#         return Foo.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super(FooTableView, self).get_context_data(**kwargs)
#         filter = FooFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
#         filter.form.helper = FooFilterFormHelper()
#         table = FooTable(filter.qs)
#         RequestConfig(self.request).configure(table)
#         context['filter'] = filter
#         context['table'] = table
#         return context
#
#
# class PagedFilteredTableView(SingleTableView):
#     filter_class = None
#     formhelper_class = None
#     context_filter_name = 'filter'
#
#     def get_queryset(self, **kwargs):
#         qs = super(PagedFilteredTableView, self).get_queryset()
#         self.filter = self.filter_class(self.request.GET, queryset=qs)
#         self.filter.form.helper = self.formhelper_class()
#         return self.filter.qs
#
#     def get_table(self, **kwargs):
#         table = super(PagedFilteredTableView, self).get_table()
#         RequestConfig(self.request, paginate={'page': self.kwargs['page'],
#                             "per_page": self.paginate_by}).configure(table)
#         return table
#
#     def get_context_data(self, **kwargs):
#         context = super(PagedFilteredTableView, self).get_context_data()
#         context[self.context_filter_name] = self.filter
#         return context
#
#
# class FooTableView(PagedFilteredTableView):
#     model = Pessoa
#     table_class = ProfissoesPessoa
#     template_name = 'app/foo_table.html'
#     paginate_by = 50
#     filter_class = Profissao
#     formhelper_class = QualificacaoProfissoesPessoa