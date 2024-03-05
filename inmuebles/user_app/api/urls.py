from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration_view, logout_view, login_view, create_superuser_view #make_admin_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'), 
    path('login-app/', login_view, name='login-app'),
    path('register/', registration_view, name='register'), 
    path('logout/', logout_view, name='logout'), 


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  

    # 2 opciones para crear superAdmin:
    #path('create-superuser/', create_superuser_view, name='create_superuser'), # yo -> opcion 1
    #path('make-admin/', make_admin_view, name='make-admin'), # yo -> opcion 2
    path('create_superuser/', create_superuser_view, name='create_superuser'),  # yo -> opcion 3
]
