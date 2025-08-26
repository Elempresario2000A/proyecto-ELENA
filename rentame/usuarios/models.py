from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
        ('moderator', 'Moderador'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user',
        verbose_name=_('Rol')
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name=_('Teléfono'))
    address = models.TextField(blank=True, verbose_name=_('Dirección'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

