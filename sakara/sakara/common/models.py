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

    def _get_full_name(self):
        "Returns the person's full name."
        return u'%s %s' % (self.nombres, self.apellidos)
    full_name = property(_get_full_name)

    # def format_birthdate(self):
    #     return self.gecha_nac.strftime('%d/%Y')[:3] + "0's"
    # decade_born_in.short_description = 'Birth decade'

    def copy_model_instance(self, obj, id):
        for f in obj._meta.fields:
            self.__setattr__(f.name, getattr(obj, f.name))
        self.id = self.pk = id
        return self

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
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


class Tipos(models.Model):
    id_servicio = models.PositiveIntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


class Subtipos(models.Model):
    id_tipo = models.PositiveIntegerField()
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

class Consulta(models.Model):
    id_cliente = models.PositiveIntegerField()
    id_servicio = models.PositiveIntegerField()
    id_tipo = models.PositiveIntegerField()
    id_subtipo = models.PositiveIntegerField()
    fecha = models.DateField()
    pago = models.FloatField()
    tipo_pago = models.CharField(max_length=50)