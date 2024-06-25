from django.contrib import admin
from .models import Usuario, Cliente, Producto, Compra, DetalleCompra, BoletaCompra

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(BoletaCompra)
