# 1

from django.urls import path
#from inmueblesList_app.api.views import inmueble_list, inmueble_detalle
from inmueblesList_app.api.views import EdificacionListAV, EdificacionDetalleAV, EmpresaAV

urlpatterns = [
    path('list/', EdificacionListAV.as_view(), name='edificacion-list'),
    path('<int:pk>', EdificacionDetalleAV.as_view(), name='edificacion-detalle'),

    path('empresa/', EmpresaAV.as_view(), name='empresa-list')
]