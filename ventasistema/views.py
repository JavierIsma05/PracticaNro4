from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Paquete, OrdenVenta

def index(request):
	context ={}
	return render(request, 'index.html', context)

def listar_ordenes_venta(request):
    ordenes_venta = OrdenVenta.objects.all()
    return render(request, 'listar_ordenes_venta.html', {'ordenes_venta': ordenes_venta})

def detalle_orden_venta(request, pk):
    orden_venta = get_object_or_404(OrdenVenta, pk=pk)
    return render(request, 'detalle_orden_venta.html', {'orden_venta': orden_venta})

def crear_orden_venta(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        nueva_orden_venta = OrdenVenta.objects.create(cliente=cliente)
        nueva_orden_venta.save()
        return redirect('detalle_orden_venta', pk=nueva_orden_venta.pk)
    else:
        clientes = Cliente.objects.all()
        return render(request, 'crear_orden_venta.html', {'clientes': clientes})

def agregar_producto_orden(request, pk):
    orden_venta = get_object_or_404(OrdenVenta, pk=pk)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = get_object_or_404(Producto, pk=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        orden_venta.productos.add(producto, through_defaults={'cantidad': cantidad})
        return redirect('detalle_orden_venta', pk=pk)
    else:
        productos = Producto.objects.all()
        return render(request, 'agregar_producto_orden.html', {'productos': productos, 'orden_venta': orden_venta})
