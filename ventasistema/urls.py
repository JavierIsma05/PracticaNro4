from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ordenes/', views.listar_ordenes_venta, name='listar_ordenes_venta'),
    path('orden/<int:pk>/', views.detalle_orden_venta, name='detalle_orden_venta'),
    path('crear_orden/', views.crear_orden_venta, name='crear_orden_venta'),
    path('orden/<int:pk>/agregar_producto/', views.agregar_producto_orden, name='agregar_producto_orden'),
    # Aquí puedes agregar más URLs según sea necesario
]