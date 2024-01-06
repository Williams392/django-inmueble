# 3

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inmueble/', include('inmueblesList_app.urls')),  # debe coincidir con el nombre de la APLICACION.
]

 # debe coincidir con el nombre de la APLICACION.