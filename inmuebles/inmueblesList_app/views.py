# 5

from django.shortcuts import render
from inmueblesList_app.models import Inmueble # para usar esta tabla.
from django.http import JsonResponse


def inmueble_list(request):
    inmuebles = Inmueble.objects.all()
    data = {
        'inmuebles': list(inmuebles.values())
    }
    return JsonResponse(data)


def inmueble_detalle(request, pk): # pk es el id.
    inmueble = Inmueble.objects.get(pk=pk)
    data = { 
        'direccion': inmueble.direccion,
        'pais': inmueble.pais,
        'imagen': inmueble.imagen,
        'active': inmueble.active,
        'descripcion': inmueble.descripcion
    }
    return JsonResponse(data)

















"""
_ Aquí está el flujo del código:

    def inmueble_list(request):

1.  inmueble = Inmueble.objects.all(): Esto crea un QuerySet que representa todos los registros en 
    la tabla Inmueble.

2.  list(inmueble.values()): Conviertes el QuerySet en una lista de diccionarios que representan 
    los valores de cada objeto en el QuerySet. El método values() se utiliza para obtener un diccionario 
    con los campos y valores de cada objeto en el QuerySet.

3.  JsonResponse(data): Devuelves una respuesta HTTP en formato JSON con la información de los 
    inmuebles. El diccionario data contiene una clave 'inmuebles' que tiene como valor la lista de 
    diccionarios obtenida del QuerySet.

    En resumen, este código devuelve todos los datos de la tabla Inmueble en formato JSON como 
    respuesta a la solicitud.
"""


"""
def inmueble_detalle(request, pk):

Crear un diccionario. Para parsear, mapear la data que me devuelve la base de datos.
"""