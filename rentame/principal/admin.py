from django.contrib import admin
from .models import Casa, ImagenCasa, Reserva, Opinion

class ImagenCasaInline(admin.TabularInline):
    model = ImagenCasa
    extra = 1

@admin.register(Casa)
class CasaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'precio_noche', 'estado', 'destacada']
    list_filter = ['estado', 'destacada', 'fecha_creacion']
    search_fields = ['nombre', 'ubicacion', 'descripcion']
    inlines = [ImagenCasaInline]

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'casa', 'fecha_inicio', 'fecha_fin', 'total', 'estado']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['usuario__username', 'casa__nombre']

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'casa', 'calificacion', 'aprobado', 'fecha_creacion']
    list_filter = ['calificacion', 'aprobado', 'fecha_creacion']
    search_fields = ['usuario__username', 'casa__nombre', 'comentario']
    list_editable = ['aprobado']  # Solo funciona si 'aprobado' está en list_display
    actions = ['aprobar_opiniones', 'rechazar_opiniones']

    def aprobar_opiniones(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, f"{queryset.count()} opiniones aprobadas.")
    
    def rechazar_opiniones(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} opiniones rechazadas.")
    
    aprobar_opiniones.short_description = "Aprobar opiniones seleccionadas"
    rechazar_opiniones.short_description = "Rechazar opiniones seleccionadas"