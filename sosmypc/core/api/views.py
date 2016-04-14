# from rest_framework import generics
from rest_framework import mixins

# Create your views here.
from rest_framework import generics #Generics
from django.contrib.auth.models import User

from sosmypc.core.api import serializers
from sosmypc.core.api.serializers import PessoaSerializer, UserSerializer, ProfissoesPessoaSerializer, \
    QualificacaoProfissoesPessoaSerializer
from sosmypc.core.models import Pessoa, ProfissoesPessoa

# #-----------------------------------------------------------------------------------------
# #Generics class based views
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# #-----------------------------------------------------------------------------------------
# #Generics class based views
# class PessoaList(generics.ListCreateAPIView):
#     queryset = Pessoa.objects.all()
#     serializer_class = PessoaSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(username=self.request.user)
#
#
# class PessoaDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Pessoa.objects.all()
#     serializer_class = PessoaSerializer
# #-----------------------------------------------------------------------------------------


#YouTube
# class HolaMundo(APIView):
#     def get(self, request, format=None):
#         return Response({'mensagem':'Hola Mundo de Django rest Framework.'})
#
# hola_mundo = HolaMundo.as_view()


# class Usuario(APIView):
#
#      serializer_class = UserSerializer
#
#      def get(selfs, request,id=None, format=None):
#          if id != None:
#              users = get_object_or_404(User,pk=id)
#              many = False
#          else:
#              users = User.objects.all()
#              many = True
#          response = selfs.serializer_class(users, many=many)
#          return Response(response.data)
#
# usuario = Usuario.as_view()

#-----------------------------------------------------------------------------------------
#Mixins


class PessoaList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class PessoaDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#-----------------------------------------------------------------------------------------
#Mixins
class ProfissoesPessoaList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = ProfissoesPessoa.objects.all()
    serializer_class = ProfissoesPessoaSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    #pessoas = serializers.PrimaryKeyRelatedField(many=True, queryset=Pessoa.objects.all())#Modificado


class ProfissoesPessoaDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = ProfissoesPessoa.objects.all()
    serializer_class = ProfissoesPessoaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#-----------------------------------------------------------------------------------------
#Mixins
class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#-----------------------------------------------------------------------------------------