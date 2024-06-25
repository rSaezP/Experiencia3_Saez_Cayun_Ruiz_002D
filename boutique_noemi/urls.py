from django.urls import path, include
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('galeria/', views.galeria, name='galeria'),
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('contacto/', views.contacto, name='contacto'),
    path('suscribir/', views.suscribir, name='suscribir'),
    path('calculadora_tallas/', views.calculadora_tallas, name='calculadora_tallas'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    path('carrito/', views.carrito, name='carrito'),  
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/cambiar-cantidad/<int:producto_id>/', views.cambiar_cantidad_carrito, name='cambiar_cantidad_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('carrito/finalizar/', views.realizar_compra, name='finalizar_compra'),  
    path('compra-exitosa/', views.compra_exitosa, name='compra_exitosa'),
]
