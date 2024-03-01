# 2:

from inmueblesList_app.models import Edificacion, Empresa, Comentario
from inmueblesList_app.api.serializers import EdificacionSerializer, EmpresaSerializer, ComentarioSerializer
from inmueblesList_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserOrReadOnly
from inmueblesList_app.api.throttling import ComentarioCreateThrottle, ComentarioListThrottle
from inmueblesList_app.api.pagination import EdificacionPagination, EdificacionLOPagination

#from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class UsuarioComentario(generics.ListAPIView): # filtro con los nombres de usuarios.
    serializer_class = ComentarioSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Comentario.objects.filter(comentario_user__username=username) # 2 rayas abajo es para acceder ala propiedad de su objeto comentario. 

    # def get_queryset(self):
    #     username = self.request.query_params.get['username', None] # cambiando para obtener desde un parametro.
    #     return Comentario.objects.filter(comentario_user__username=username)
    
class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ComentarioCreateThrottle]
    
    def get_queryset(self):
        return Comentario.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Edificacion.objects.get(pk=pk)

        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble, comentario_user=user)

        if comentario_queryset.exists(): # exists -> es si existe data
            raise ValidationError("El usuario ya escribio un comentario para este inmueble")
        
        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = serializer.validated_data['calificacion']
        else:
            inmueble.avg_calificacion = (serializer.validated_data['calificacion'] + inmueble.avg_calificacion/2)

        inmueble.number_calificacion = inmueble.number_calificacion + 1
        inmueble.save()

        serializer.save(edificacion=inmueble, comentario_user=user)

# ---------------------------------------------------------------------------------------------------
# Otra forma mejor de usar estos 2 metodos GENERICOS: 
# ---------------------------------------------------------------------------------------------------
class ComentarioList(generics.ListCreateAPIView):
    #queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    #permission_classes = [IsAuthenticated] # solo los usuarios logeados.
    #throttle_classes = [UserRateThrottle, AnonRateThrottle] # limitando los numeros de request.
    throttle_classes = [ComentarioListThrottle, AnonRateThrottle] # este es un throttle PERSONALIZADO.
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)

class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView): # Busqueda por id y Update
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    permission_classes = [IsComentarioUserOrReadOnly]
    #throttle_classes = [UserRateThrottle, AnonRateThrottle] # limitando los numeros de request
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comentario-detail'

# class ComentarioList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self, request, *args, **kwargs): 
#         return self.list(request, *args, **kwargs) # método genérico que va a disparar un evento interno para generar el response 

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ComentarioDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self, request, *args, **kwargs): 
#         return self.retrieve(request, *args, **kwargs)
# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------
# Con este metodo de 3 lineas actualiza, elimina, crea y busca por id.
    # . Solo para mantenimientos genericos, No para logica de NEgocio oh a varias entidades.
# ---------------------------------------------------------------------------------------------------
class EmpresaVS(viewsets.ModelViewSet): 

    permission_classes = [IsAdminOrReadOnly] # el Admi viene desde -> ( api/permission )

    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

# class EmpresaVS(viewsets.ViewSet): # ViewSet
#     def list(self, request):
#         queryset = Empresa.objects.all()
#         serializer = EmpresaSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = Empresa.objects.all()
#         edificacionList = get_object_or_404(queryset, pk=pk)
#         serializer = EmpresaSerializer(edificacionList)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = EmpresaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = EmpresaSerializer(empresa, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
#         empresa.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# ---------------------------------------------------------------------------------------------------

class EmpresaAV(APIView):

    def get(self, request):
        empresas = Empresa.objects.all()
        serializer = EmpresaSerializer(empresas, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class EmpresaDetalleAV(APIView):

    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = EmpresaSerializer(empresa, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaSerializer(empresa, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# ---------------------------------------------------------------------------------------------------
        

class EdifacionList(generics.ListAPIView): # filtro para buscar.
    queryset = Edificacion.objects.all()
    serializer_class = EdificacionSerializer

    #filter_backends = [DjangoFilterBackend] # la busqueda debe de ser nombre completo.
    # filterset_fields = ['direccion', 'empresa__nombre'] # siempre 2 barras abajo para llamar al objeto de la BD

    filter_backends = [filters.SearchFilter, filters.OrderingFilter] # las busqueda mas rapida no necesita compretar todo.
    search_fields = ['direccion', 'empresa__nombre']
    pagination_class = EdificacionPagination
    #pagination_class =  EdificacionLOPagination



class EdificacionAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        edificacion = Edificacion.objects.all()
        serializer = EdificacionSerializer(edificacion, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdificacionSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save() 
             return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EdificacionDetalleAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk): # buscar un inmueble por su id
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EdificacionSerializer(edificacion)
        return Response(serializer.data)

    def put(self, request, pk): 
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EdificacionSerializer(edificacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk): 
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'Error': 'Inmueble no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        edificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    


































# @api_view(['GET', 'POST'])
    
# def inmueble_list(request):

#     if request.method == 'GET':
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         de_serializer = InmuebleSerializer(data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save() 
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def inmueble_detalle(request, pk):

#     if request.method == 'GET': # buscar un inmueble por su id
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             serializer = InmuebleSerializer(inmueble)
#             return Response(serializer.data)
#         except Inmueble.DoesNotExist:
#             return Response({'Error': 'El inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         inmueble = Inmueble.objects.get(pk=pk)
#         de_serializer = InmuebleSerializer(inmueble, data=request.data)
#         if de_serializer.is_valid():
#             de_serializer.save()
#             return Response(de_serializer.data)
#         else:
#             return Response(de_serializer.errors, status=status.HTTP_400_BAD_REQUEST) # cuando es data ERRONEA

#     if request.method == 'DELETE':
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             inmueble.delete()
#         except Inmueble.DoesNotExist:
#             return Response({'Error': 'El inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     if request.method == 'DELETE':
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             inmueble.delete()
#         except Inmueble.DoesNotExist:
#             return Response({'Error': 'El inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response(status=status.HTTP_204_NO_CONTENT)