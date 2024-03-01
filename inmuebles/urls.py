# 3

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', include('inmueblesList_app.api.urls')),  # debe coincidir con el nombre de la APLICACION.
    path('account/', include('user_app.api.urls')),
    # path('api-auth', include('rest_framework.urls')), # activa una pantalla de login para el rest_framework
]

 # debe coincidir con el nombre de la APLICACION.