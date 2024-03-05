from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
# from user_app import models
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 

from django.contrib.auth.hashers import check_password
from user_app.models import Account
from django.contrib import auth

# ----------------------------------------------------------------------------------------
from rest_framework.decorators import permission_classes # yo
from rest_framework.permissions import IsAdminUser # yo
from user_app.models import MyAccountManager # yo


# Opcion 1 -> para convertir en administrador:

# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def create_superuser_view(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not all([username, first_name, last_name, email, password]):
#             return Response({'error': 'Todos los campos son obligatorios'}, status=400)

#         try:
#             user_manager = MyAccountManager()
#             user_manager.create_superuser(first_name, last_name, email, username, password)
#             return Response({'message': 'Superadmin creado exitosamente'}, status=201)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)

# Opcion 2 -> para convertir en administrador:
# from django.http import JsonResponse

# @api_view(['POST'])
# def make_admin_view(request):
#     if request.method == 'POST':
#         username = request.data.get('username', None)
#         if not username:
#             return JsonResponse({'error': 'Se requiere el nombre de usuario para convertirlo en administrador.'}, status=400)
        
#         try:
#             user = Account.objects.get(username=username)
#             user.is_admin = True
#             user.save()
#             return JsonResponse({'success': f'El usuario {username} ha sido convertido en administrador.'}, status=200)
#         except Account.DoesNotExist:
#             return JsonResponse({'error': 'El usuario especificado no existe.'}, status=404)

# Opcion 3:
        
from .serializers import CreateSuperUserSerializer

@api_view(['POST'])
def create_superuser_view(request):
    if request.method == 'POST':
        serializer = CreateSuperUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Superusuario creado correctamente.", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------

# salir de sesion:
@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# Resgistro de nuevo usuario y token de seguridad:
@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'El registro del usuario fue exitoso'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['phone_number'] = account.phone_number
            # token = Token.objects.get(user=account).key
            # data['token'] = token

            refresh = RefreshToken.for_user(account) # ya no seguridad de 'token' a hora 'RefreshToken'
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data)

        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Metodo login:       
@api_view(['POST'])
def login_view(request):
    data = {}
    if request.method=='POST':
        email = request.data.get('email')
        password = request.data.get('password')

        account = auth.authenticate(email=email, password=password) # Proceso de authentificacion.
        if account is not None: 
            # si las 2 credenciales son correctas me devuelve esto ->
            data['response']='El Login fue exitoso'
            data['username']=account.username
            data['email']=account.email
            data['first_name']=account.first_name
            data['last_name']=account.last_name
            data['phone_number']=account.phone_number
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data)
        else:
            data['error'] = "Credenciales incorrectas"
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)