from django.shortcuts import render

# Create your views here.
# sosmypc/financeiro/views.py
# from django.core import serializers
# from django.http import HttpResponse
# from django.shortcuts import render
# from sosmypc.financeiro.models import Conta
# from sosmypc.core.models import Pessoa


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from sosmypc.financeiro.models import ContaPagar, ContaReceber, CONTA_STATUS_APAGAR


def contas(request):
    contas_a_pagar = ContaPagar.objects.filter(
        status=CONTA_STATUS_APAGAR,
        )
    contas_a_receber = ContaReceber.objects.filter(
        status=CONTA_STATUS_APAGAR,
        )

    return render_to_response(
        'contas/contas.html',
        locals(),
        context_instance=RequestContext(request),
        )

def conta(request, conta_id, classe):
    conta = get_object_or_404(classe, id=conta_id)
    return render_to_response(
        'contas/conta.html',
        locals(),
        context_instance=RequestContext(request),
        )

# def lista(request):
#     context = {
#         'pessoas': Pessoa.objects.using('default').all()
#     }
#     return render(request, 'exemplo.html', context)
#
#
# def json_contas(request, id_pessoa):
#     """
#     Método responsável por popular a lista
#     :param request:
#     :param id:
#     :return HttpResponse:
#     """
#
#     obj = Conta.objects.using('default').filter(pessoa=id_pessoa)
#     retorno = serializers.serialize('json', obj)
#     return HttpResponse(retorno, content_type='application/json')