from django.contrib import admin
from sosmypc.core.models import Pessoa, Profissao, ProfissoesPessoa, Qualificacao, QualificacaoProfissoesPessoa#, Comentarios, QualificacaoProfissoesPessoa


class PessoaModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('nomepessoa', 'tipologradouro','numero', 'bairro', 'cidade', 'estado')


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
    list_select_related = True
    #list_display = ('pessoa','profissoes',  'rating')


class QualificacoesModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('id','descricao')


class QualificacoesProfissoesPessoaModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('pessoa__nome','qualificacao','profissaopessoa')

    def pessoa__nome(self, obj):
        return obj.profissaopessoa.pessoa.nomepessoa.upper()
    pessoa__nome.short_description = u'NOME'


# Register your models here.
admin.site.register(Pessoa, PessoaModelAdmin)
#admin.site.register(Tecnico, TecnicoModelAdmin)
admin.site.register(Qualificacao, QualificacoesModelAdmin)
admin.site.register(QualificacaoProfissoesPessoa, QualificacoesProfissoesPessoaModelAdmin)
admin.site.register(ProfissoesPessoa, ProfissoesPessoaModelAdmin)
admin.site.register(Profissao)
#admin.site.register(Comentarios, ComentariosModelAdmin)