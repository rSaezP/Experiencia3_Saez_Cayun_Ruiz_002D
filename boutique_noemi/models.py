from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.conf import settings

from django.conf import settings

class Usuario(AbstractUser):
    es_administrador = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='usuario',
    )

    def __str__(self):
        return self.username


class Cliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    celular = models.CharField(max_length=15)
    intereses_choices = [
        ('niño', 'Niño'),
        ('niña', 'Niña'),
        ('recien_nacido', 'Recién Nacido'),
    ]
    intereses = models.CharField(max_length=20, choices=intereses_choices)

    def __str__(self):
        return self.user.username 

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=100)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def aumentar_stock(self, cantidad):
        self.stock += cantidad
        self.save()

    def reducir_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False

class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado_choices = [
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=20, choices=estado_choices, default='en_proceso')

    def __str__(self):
        return f"Compra #{self.id} - {self.cliente.user.username}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, default=1 )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Detalle {self.id} - Compra {self.compra.id}"
    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class BoletaCompra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    detalles = models.ManyToManyField(DetalleCompra)

    def __str__(self):
        return f"Boleta #{self.id} - {self.cliente.user.username}"

    def productos_comprados(self):
        detalles = self.detallecompra_set.all()
        return [(detalle.producto, detalle.cantidad) for detalle in detalles]
    
    
    