from django.contrib import admin
from sosmypc.core.models import Pessoa, Profissao, ProfissoesPessoa, Qualificacao, QualificacaoProfissoesPessoa#, Comentarios, QualificacaoProfissoesPessoa


class PessoaModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('nomepessoa', 'tipologradouro','numero', 'bairro', 'cidade', 'estado')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PessoaModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['username'].initial = request.user.pk
        return form


class TecnicoModelAdmin(admin.ModelAdmin):
    #list_select_related = True
    list_display = ('longitude','latitude',  'classificacao', 'especificacao_tecnico')


class ComentariosModelAdmin(admin.ModelAdmin):
    #list_select_related = True
    list_display = ('pessoa__nome','nomepessoa', 'profissaopessoa','comentario',  'rating')

    def pessoa__nome(self, obj):
        return obj.profissaopessoa.pessoa.nomepessoa.upper()
    pessoa__nome.short_description = u'NOME'

class ProfissoesPessoaModelAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'profissao')
    #exclude = ['pessoa',]
    def get_form(self, request, obj=None, **kwargs):#Seta apessoa logada no template do admin
        # print('GET_FORM_>>>>>>  ', request.user.pessoa  )
        form = super(ProfissoesPessoaModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['pessoa'].initial = request.user.pk
        return form
    def get_queryset(self, request):# Filtra registros somente da pessoa logada
        qs = super(ProfissoesPessoaModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pessoa__username=request.user)

class QualificacoesModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('id','descricao')


class QualificacoesProfissoesPessoaModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('pessoa__nome','qualificacao','profissao')

    def pessoa__nome(self, obj):
        return obj.profissao.pessoa.nomepessoa.upper()
    pessoa__nome.short_description = u'NOME'


# Register your models here.
admin.site.register(Pessoa, PessoaModelAdmin)
#admin.site.register(Tecnico, TecnicoModelAdmin)
admin.site.register(Qualificacao, QualificacoesModelAdmin)
admin.site.register(QualificacaoProfissoesPessoa, QualificacoesProfissoesPessoaModelAdmin)
admin.site.register(ProfissoesPessoa, ProfissoesPessoaModelAdmin)
admin.site.register(Profissao)
#admin.site.register(Comentarios, ComentariosModelAdmin)