# 1

from django.urls import path
#from inmueblesList_app.api.views import inmueble_list, inmueble_detalle
from inmueblesList_app.api.views import EdificacionListAV, EdificacionDetalleAV, EmpresaAV, EmpresaDetalleAV, ComentarioList, ComentarioDetail

urlpatterns = [
    path('list/', EdificacionListAV.as_view(), name='edificacion'),
    path('<int:pk>', EdificacionDetalleAV.as_view(), name='edificacion-detail'),

    path('empresa/', EmpresaAV.as_view(), name='empresa'),
    path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name='empresa-detail'), # En django es muy importante es la nomenclatura -> por eso importante poner en INGLES.

    path('comentario/', ComentarioList.as_view(), name='comentario-list'),
    path('comentario/<int:pk>', ComentarioDetail.as_view(), name='comentario-detail'),
]