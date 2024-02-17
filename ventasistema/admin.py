from django.contrib import admin
from .models import Cliente, Producto, Paquete, OrdenVenta, OrdenProducto, ComprobantePago

class OrdenProductoInline(admin.TabularInline):
    model = OrdenProducto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields=['nombre', 'dni']
    list_display = ['id', 'nombre', 'dni', 'direccion']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio']

@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

@admin.register(OrdenVenta)
class OrdenVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado']
    search_fields=['cliente', 'estado']
    inlines = [OrdenProductoInline]

@admin.register(OrdenProducto)
class OrdenProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'orden', 'producto', 'cantidad']


class ComprobantePagoAdmin(admin.ModelAdmin):
    list_display = ('orden', 'numero_secuencia', 'fecha_emision', 'total')
    search_fields = ['orden__cliente__nombre', 'numero_secuencia']
    list_filter = ('fecha_emision',)

admin.site.register(ComprobantePago, ComprobantePagoAdmin)
