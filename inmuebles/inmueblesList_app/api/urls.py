# 1

from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from inmueblesList_app.api.views import inmueble_list, inmueble_detalle
from inmueblesList_app.api.views import (EdificacionListAV, EdificacionDetalleAV, EmpresaAV, EmpresaDetalleAV, 
                                         ComentarioList, ComentarioDetail, ComentarioCreate, EmpresaVS)

router = DefaultRouter()
router.register('empresa', EmpresaVS, basename='empresa')

urlpatterns = [
    path('edificacion/', EdificacionListAV.as_view(), name='edificacion'),
    path('edificacion/<int:pk>', EdificacionDetalleAV.as_view(), name='edificacion-detail'),


    path('', include(router.urls)),
    # path('empresa/', EmpresaAV.as_view(), name='empresa'),
    # path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name='empresa-detail'), # En django es muy importante es la nomenclatura -> por eso importante poner en INGLES.

    path('edificacion/<int:pk>/comentario-create/', ComentarioCreate.as_view(), name='comentario-create'), # insertar new comentarios
    path('edificacion/<int:pk>/comentario/', ComentarioList.as_view(), name='comentario-list'),
    path('comentario/<int:pk>', ComentarioDetail.as_view(), name='comentario-detail'),
]