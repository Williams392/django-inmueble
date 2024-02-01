# 2

from django.contrib import admin
from inmueblesList_app.models import Edificacion, Empresa, Comentario # importando el objeto desde MODELS.

admin.site.register(Edificacion) # agregando la estructura a la aplicacion
admin.site.register(Empresa)
admin.site.register(Comentario)

