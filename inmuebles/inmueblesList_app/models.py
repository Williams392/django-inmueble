# 1
# primera estructura que muestra que presenta a un inmueble:

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Empresa(models.Model):
    nombre = models.CharField(max_length = 250)
    website = models.URLField(max_length = 250)
    active = models.BooleanField(default = True)

    def __str__(self) -> str:
        return self.nombre

class Edificacion(models.Model):
    direccion = models.CharField(max_length = 250)
    pais = models.CharField(max_length = 150)
    descripcion = models.CharField(max_length = 500)
    imagen = models.CharField(max_length = 900)
    active = models.BooleanField( default = True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="edificacionList") 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.direccion} - {self.pais}" # quiero que retorne para q muestre como indice el elemento guardado.

class Comentario(models.Model):
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    texto = models.CharField( max_length = 200, null=True )
    edificacion = models.ForeignKey(Edificacion, on_delete=models.CASCADE, related_name="comentarios")
    active = models.BooleanField( default = True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.calificacion) + " - " + self.edificacion.direccion # no muestra el nombre dire en el Admin

# 1. python manage.py makemigrations
# 2. python manage.py migrate