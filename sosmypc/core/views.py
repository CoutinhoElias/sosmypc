from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from sosmypc import settings
from sosmypc.core.forms import CommentForm, RegistrationForm
from sosmypc.core.models import ProfissoesPessoa, QualificacaoProfissoesPessoa, Profissao
from sosmypc.settings import LOGIN_URL

import extra_views
from material import LayoutMixin, Layout, Fieldset, Inline, Row, Span2, Span5, Span7

# #Utilizado na classe FormsetMixin
# from django.views.generic import CreateView, ListView, DetailView, UpdateView
# from django.shortcuts import redirect
# #-----------------------------------------------------------------------------
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from sosmypc.core.models import Pessoa
import urllib, json

# Create your views here.....

#import pdb; pdb.set_trace()
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
#Funções utilizadas para Autenticação e validação.
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
    profissoespessoa = ProfissoesPessoa.objects.filter(pessoa__username=request.user)

    return render(request,'sosmypc/person_and_professions.html',{'profissoespessoa':profissoespessoa})


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

            return render(request, 'registration.html',
                          {
                              'form': RegistrationForm(),
                          })
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


#----------------------------------------------------------------------------------------------------------------------
#Classes utilizadas para formulários InlinrFormset
# class FormsetMixin(object):
#     object = None
#
#     def get(self, request, *args, **kwargs):
#         if getattr(self, 'is_update_view', False):
#             self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         formset_class = self.get_formset_class()
#         formset = self.get_formset(formset_class)
#         return self.render_to_response(self.get_context_data(form=form, formset=formset))
#
#     def post(self, request, *args, **kwargs):
#         if getattr(self, 'is_update_view', False):
#             self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         formset_class = self.get_formset_class()
#         formset = self.get_formset(formset_class)
#         if form.is_valid() and formset.is_valid():
#             return self.form_valid(form, formset)
#         else:
#             return self.form_invalid(form, formset)
#
#     def get_formset_class(self):
#         return self.formset_class
#
#     def get_formset(self, formset_class):
#         return formset_class(**self.get_formset_kwargs())
#
#     def get_formset_kwargs(self):
#         kwargs = {
#             'instance': self.object
#         }
#         if self.request.method in ('POST', 'PUT'):
#             kwargs.update({
#                 'data': self.request.POST,
#                 'files': self.request.FILES,
#             })
#         return kwargs
#
#     def form_valid(self, form, formset):
#         self.object = form.save()
#         formset.instance = self.object
#         formset.save()
#         return redirect(self.object.get_absolute_url())
#
#     def form_invalid(self, form, formset):
#         return self.render_to_response(self.get_context_data(form=form, formset=formset))
#
#
# class ProfissoesPessoaCreateView(FormsetMixin, CreateView):
#     template_name = 'sosmypc/person_and_professions_form.html'
#     model = ProfissoesPessoa
#     form_class = ProfissoesPessoaForm
#     formset_class = QualificacaoProfissoesPessoaFormSet
#
#
# class ProfissoesPessoaUpdateView(FormsetMixin, UpdateView):
#     template_name = 'books/author_and_books_form.html'
#     is_update_view = True
#     model = ProfissoesPessoa
#     form_class = ProfissoesPessoaForm
#     formset_class = QualificacaoProfissoesPessoaFormSet
#
#
# class QualificacaoProfissoesPessoaList(ListView):
#
#     model = QualificacaoProfissoesPessoa
#
#
# class QualificacaoProfissoesPessoaDetail(DetailView):
#
#     model = QualificacaoProfissoesPessoa
#
#
# class ProfissoesPessoaList(ListView):
#
#     model = ProfissoesPessoa
#
#
# class ProfissoesPessoaDetail(DetailView):
#
#     model = ProfissoesPessoa

#----------------------------------------------------------------------------------------------------------------------
#Classes utilizadas para formulários InlinrFormset
# def submit_recipe(request):
#     if request.POST:
#
#         form = UserSubmittedRecipeForm(request.POST)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
#             if ingredient_formset.is_valid():
#                 recipe.save()
#                 ingredient_formset.save()
#                 return HttpResponseRedirect(reverse('recipes_submit_posted'))
#     else:
#         form = UserSubmittedRecipeForm()
#         ingredient_formset = IngredientFormSet(instance=Recipe())
#     return render_to_response('sosmypc/person_and_professions_form.html', {
#         "form": form,
#         "ingredient_formset": ingredient_formset,
#     }, context_instance=RequestContext(request))

# def profissoesPessoa(request):
#     profissoes_pessoa = ProfissoesPessoa()
#     qualificacao_profissao_pessoa_formset = inlineformset_factory(ProfissoesPessoa, QualificacaoProfissoesPessoa, form=QualificacaoProfissoesPessoaForm,fields='__all__', extra=1, can_delete=False,
#                                                min_num=1, validate_min=True)
#
#     if request.method == 'POST':
#         forms = ProfissoesPessoaForm(request.POST, request.FILES, instance=profissoes_pessoa, prefix='main')
#         formset = qualificacao_profissao_pessoa_formset(request.POST, request.FILES, instance=profissoes_pessoa, prefix='qualificacao')
#
#         if forms.is_valid() and formset.is_valid():
#             forms = forms.save(commit=False)
#             forms.save()
#             formset.save()
#             return HttpResponseRedirect('/person_and_professions.html')
#
#     else:
#         forms = ProfissoesPessoaForm(instance=profissoes_pessoa, prefix='profissoes')
#         formset = qualificacao_profissao_pessoa_formset(instance=profissoes_pessoa, prefix='qualificacao')
#
#     context = {
#         'forms': forms,
#         'formset': formset,
#     }
#
#     return render(request, 'sosmypc/person_and_professions.html', context)



#-----------------------------------------------------------------------------------------------------------------------
class ItemInline(extra_views.InlineFormSet):
    model = QualificacaoProfissoesPessoa
    fields = ['id', 'qualificacao']


class NewProfissoesPessoaView(LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.CreateWithInlinesView):
    title = "Nova Profissão"
    model = ProfissoesPessoa
    layout = Layout(
        Row('pessoa', 'profissao', 'rating'),
        # Fieldset('Address',
        #          Row(Span7('address'), Span5('zipcode')),
        #          Row(Span5('city'), Span2('state'), Span5('country'))),
        Inline('Qualificações da Profissão', ItemInline),
    )


























