from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    nombre = models.CharField(max_length=100)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return self.nombre
# STATE PATRON
class EstadoOrden:
    def procesar_orden(self, orden):
        raise NotImplementedError()

class EstadoBorrador(EstadoOrden):
    def procesar_orden(self, orden):
        # Lógica para procesar una orden en estado "Borrador"
        orden.estado = 'borrador'
        orden.save()
        # Aquí podrías realizar otras acciones específicas para este estado

class EstadoAceptado(EstadoOrden):
    def procesar_orden(self, orden):
        # Lógica para procesar una orden en estado "Aceptado"
        orden.estado = 'aceptado'
        orden.save()
        # Aquí podrías realizar otras acciones específicas para este estado

class EstadoArchivado(EstadoOrden):
    def procesar_orden(self, orden):
        # Lógica para procesar una orden en estado "Archivado"
        orden.estado = 'archivado'
        orden.save()
        # Aquí podrías realizar otras acciones específicas para este estado

class OrdenVenta(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('aceptado', 'Aceptado'),
        ('archivado', 'Archivado'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    productos = models.ManyToManyField(Producto, through='OrdenProducto')
    paquetes = models.ManyToManyField(Paquete, blank=True)

    def __str__(self):
        return f"OrdenVenta #{self.id} - {self.cliente}"

    def procesar(self):
        if self.estado == 'borrador':
            estado = EstadoBorrador()
        elif self.estado == 'aceptado':
            estado = EstadoAceptado()
        elif self.estado == 'archivado':
            estado = EstadoArchivado()
        estado.procesar_orden(self)

class OrdenProducto(models.Model):
    orden = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.producto} - Cantidad: {self.cantidad}"

class ComprobantePago(models.Model):
    orden = models.OneToOneField(OrdenVenta, on_delete=models.CASCADE, related_name='comprobante_pago')
    numero_secuencia = models.IntegerField(unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.FloatField()

    def __str__(self):
        return f"Comprobante de Pago - Orden #{self.orden.id}"

    def generar_comprobante(self):
        if self.orden.estado == 'aceptado':
            # Lógica para generar el comprobante de pago basado en la orden de venta
            total = sum(orden_producto.producto.precio * orden_producto.cantidad for orden_producto in self.orden.ordenproducto_set.all())
            self.total = total
            self.save()
            return True
        else:
            return False

    def imprimir(self):
        # Lógica para imprimir el comprobante de pago (simulada)
        return f"Comprobante de Pago - Orden #{self.orden.id}\nFecha de Emisión: {self.fecha_emision}\nTotal: {self.total}"

