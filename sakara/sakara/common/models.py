from django.db import models

# Create your models here.
class Clientes(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    fecha_nac = models.DateTimeField()
    direccion = models.CharField(max_length=100)
    email = models.EmailField()
    observaciones = models.CharField(max_length=200)


class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


class VentaProducto(models.Model):
    id_cliente = models.PositiveIntegerField()
    id_producto = models.PositiveIntegerField()
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    pago = models.FloatField()


class Servicios(models.Model):
    id_servicio = models.PositiveIntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


class Tipos(models.Model):
    id_tipo = models.PositiveIntegerField()
    id_servicio = models.PositiveIntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


class Subtipos(models.Model):
    id_subtipo = models.PositiveIntegerField()
    id_tipo = models.PositiveIntegerField()
    nombre = models.CharField(max_length=50)


class Consulta(models.Model):
    id_consulta = models.PositiveIntegerField()
    id_cliente = models.PositiveIntegerField()
    id_servicio = models.PositiveIntegerField()
    id_tipo = models.PositiveIntegerField()
    id_subtipo = models.PositiveIntegerField()
    fecha = models.DateField()
    pago = models.FloatField()
    tipo_pago = models.CharField(max_length=50)