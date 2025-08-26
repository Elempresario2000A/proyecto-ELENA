from django.db import models
from django.conf import settings  # 👈 Importamos para usar el CustomUser configurado
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Casa(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=300)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    imagen_principal = models.ImageField(upload_to='casas/')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    destacada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre


class ImagenCasa(models.Model):
    casa = models.ForeignKey(Casa, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='casas/galeria/')
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Imagen de {self.casa.nombre}"


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 👈 Usamos CustomUser
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.casa.nombre} por {self.usuario}"


class Opinion(models.Model):
    casa = models.ForeignKey('Casa', on_delete=models.CASCADE, related_name='opiniones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ← CORREGIDO
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación del 1 al 5"
    )
    comentario = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_creacion']
        unique_together = ['casa', 'usuario']
    
    def __str__(self):
        return f"Opinión de {self.usuario.username} para {self.casa.nombre}"

class Promocion(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name='promociones')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    imagen = models.ImageField(upload_to='promociones/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.casa.nombre}"