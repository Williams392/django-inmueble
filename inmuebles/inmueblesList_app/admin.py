# 2

from django.contrib import admin
from inmueblesList_app.models import Edificacion, Empresa # importando el objeto Inmueble

admin.site.register(Edificacion) # agregando la estructura a la aplicacion
admin.site.register(Empresa)

