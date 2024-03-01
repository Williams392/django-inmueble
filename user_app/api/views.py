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