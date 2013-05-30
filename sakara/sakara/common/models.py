from django.db import models


# Create your models here.
class Clientes(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    fecha_nac = models.DateField()
    direccion = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=9, blank=True)
    movil = models.CharField(max_length=9, blank=True)
    fecha_alta = models.DateField()
    observaciones = models.CharField(max_length=200, blank=True)


class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)


class VentaProducto(models.Model):
    id_cliente = models.PositiveIntegerField()
    id_producto = models.PositiveIntegerField()
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    pago = models.FloatField()


class Servicios(models.Model):
    padre = models.PositiveIntegerField(max_length=5)
    nivel = models.PositiveIntegerField(max_length=5)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)


class Consulta(models.Model):
    id_cliente = models.PositiveIntegerField()
    id_servicio = models.PositiveIntegerField()
    id_tipo = models.PositiveIntegerField()
    id_subtipo = models.PositiveIntegerField()
    fecha = models.DateField()
    pago = models.FloatField()
    tipo_pago = models.CharField(max_length=50)