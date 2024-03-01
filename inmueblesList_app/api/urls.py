# 1

from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from inmueblesList_app.api.views import inmueble_list, inmueble_detalle
from inmueblesList_app.api.views import (EdificacionAV, EdificacionDetalleAV, EmpresaAV, EmpresaDetalleAV, ComentarioList,
                                        ComentarioDetail, ComentarioCreate, EmpresaVS, UsuarioComentario, EdifacionList)

router = DefaultRouter()
router.register('empresa', EmpresaVS, basename='empresa')

urlpatterns = [
    path('edificacion/', EdificacionAV.as_view(), name='edificacion'),
    path('edificacion/list/', EdifacionList.as_view(), name='edificacion-list'),
    path('edificacion/<int:pk>', EdificacionDetalleAV.as_view(), name='edificacion-detail'),


    path('', include(router.urls)),
    # path('empresa/', EmpresaAV.as_view(), name='empresa'),
    # path('empresa/<int:pk>', EmpresaDetalleAV.as_view(), name='empresa-detail'), # En django es muy importante es la nomenclatura -> por eso importante poner en INGLES.

    path('edificacion/<int:pk>/comentario-create/', ComentarioCreate.as_view(), name='comentario-create'), # insertar new comentarios
    path('edificacion/<int:pk>/comentario/', ComentarioList.as_view(), name='comentario-list'),
    path('edificacion/comentario/<int:pk>', ComentarioDetail.as_view(), name='comentario-detail'),

    path('edificacion/comentarios/<str:username>', UsuarioComentario.as_view(), name='usuario-comentario-detail'),
]