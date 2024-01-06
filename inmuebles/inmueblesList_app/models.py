# 1
# primera estructura que muestra que presenta a un inmueble:

from django.db import models

class Inmueble(models.Model):
    direccion = models.CharField(max_length = 250)
    pais = models.CharField(max_length = 150)
    descripcion = models.CharField(max_length = 500)
    imagen = models.CharField(max_length = 900)
    active = models.BooleanField( default = True)

    def __str__(self) -> str:
        return f"{self.direccion} - {self.pais}" # quiero que retorne para q muestre como indice el elemento guardado.

# 1. python manage.py makemigrations
# 2. python manage.py migrate