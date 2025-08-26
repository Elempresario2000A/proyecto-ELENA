from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .models import Casa, ImagenCasa, Opinion
from .forms import CasaForm, ImagenCasaForm, OpinionForm, PromocionForm
from django.db.models import Avg, Count
from django.shortcuts import render
from .models import Opinion, Casa, Promocion

def Principal(request):
    return render(request, 'inicio/principal.html')

def Opiniones(request):
    return render(request, 'inicio/opiniones.html')

def Contacto(request):
    return render(request, 'inicio/contacto.html')
# Función para verificar si es admin
def es_administrador(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

# Lista de casas (accesible para todos)
def lista_casas(request):
    casas = Casa.objects.filter(estado='disponible')
    return render(request, 'inicio/lista_casas.html', {'casas': casas})

# Detalle de casa (accesible para todos)
def detalle_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    return render(request, 'inicio/detalles_casa.html', {'casa': casa})

# Crear casa (solo admin)
@login_required
@user_passes_test(es_administrador)
def crear_casa(request):
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES)
        if form.is_valid():
            casa = form.save()
            messages.success(request, f'Casa "{casa.nombre}" creada exitosamente!')
            return redirect('casas:lista_casas')
    else:
        form = CasaForm()
    return render(request, 'inicio/crear_casa.html', {'form': form})

# Editar casa (solo admin)
@login_required
@user_passes_test(es_administrador)
def editar_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    if request.method == 'POST':
        form = CasaForm(request.POST, request.FILES, instance=casa)
        if form.is_valid():
            casa = form.save()
            messages.success(request, f'Casa "{casa.nombre}" actualizada exitosamente!')
            return redirect('casas:detalle_casa', casa_id=casa.id)
    else:
        form = CasaForm(instance=casa)
    return render(request, 'inicio/editar_casa.html', {'form': form, 'casa': casa})

# Eliminar casa (solo admin)
@login_required
@user_passes_test(es_administrador)
def eliminar_casa(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    if request.method == 'POST':
        nombre_casa = casa.nombre
        casa.delete()
        messages.success(request, f'Casa "{nombre_casa}" eliminada exitosamente!')
        return redirect('casas:lista_casas')
    return render(request, 'inicio/eliminar_casa.html', {'casa': casa})

@login_required
def crear_opinion(request, casa_id):
    casa = get_object_or_404(Casa, id=casa_id)
    
    # Verificar si el usuario ya opinó sobre esta casa
    opinion_existente = Opinion.objects.filter(casa=casa, usuario=request.user).first()
    
    if opinion_existente:
        messages.warning(request, 'Ya has publicado una opinión para esta casa.')
        return redirect('casas:detalle_casa', casa_id=casa_id)
    
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.casa = casa
            opinion.usuario = request.user
            
            # Si el usuario es admin, aprobar automáticamente
            if request.user.is_superuser or request.user.is_staff:
                opinion.aprobado = True
            
            opinion.save()
            messages.success(request, '¡Tu opinión ha sido publicada!')
            return redirect('casas:detalle_casa', casa_id=casa_id)
    else:
        form = OpinionForm()
    
    return render(request, 'inicio/crear_opinion.html', {
        'form': form, 
        'casa': casa
    })

@login_required
def mis_opiniones(request):
    opiniones = Opinion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'inicio/mis_opiniones.html', {'opiniones': opiniones})

@login_required
def editar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id, usuario=request.user)
    
    if request.method == 'POST':
        form = OpinionForm(request.POST, instance=opinion)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu opinión ha sido actualizada!')
            return redirect('casas:mis_opiniones')
    else:
        form = OpinionForm(instance=opinion)
    
    return render(request, 'inicio/editar_opinion.html', {
        'form': form, 
        'opinion': opinion
    })

@login_required
def eliminar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id, usuario=request.user)
    
    if request.method == 'POST':
        casa_id = opinion.casa.id
        opinion.delete()
        messages.success(request, '¡Tu opinión ha sido eliminada!')
        return redirect('casas:mis_opiniones')
    
    return render(request, 'inicio/eliminar_opinion.html', {'opinion': opinion})

# Vista para administradores - moderar opiniones
@login_required
@user_passes_test(es_administrador)
def moderar_opiniones(request):
    opiniones_pendientes = Opinion.objects.filter(aprobado=False).order_by('-fecha_creacion')
    return render(request, 'inicio/moderar_opiniones.html', {
        'opiniones_pendientes': opiniones_pendientes
    })

@login_required
@user_passes_test(es_administrador)
def aprobar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id)
    
    if request.method == 'POST':
        opinion.aprobado = True
        opinion.save()
        messages.success(request, f'Opinión de {opinion.usuario.username} aprobada.')
    
    return redirect('casas:moderar_opiniones')

@login_required
@user_passes_test(es_administrador)
def rechazar_opinion(request, opinion_id):
    opinion = get_object_or_404(Opinion, id=opinion_id)
    
    if request.method == 'POST':
        opinion.delete()
        messages.success(request, f'Opinión de {opinion.usuario.username} rechazada.')
    
    return redirect('casas:moderar_opiniones')

def opiniones(request):
    # Obtener opiniones aprobadas
    opiniones_aprobadas = Opinion.objects.filter(aprobada=True).select_related('usuario', 'casa')
    
    # Estadísticas
    promedio_calificacion = Opinion.objects.filter(aprobada=True).aggregate(
        Avg('calificacion')
    )['calificacion__avg']
    
    total_opiniones = Opinion.objects.filter(aprobada=True).count()
    
    # Porcentaje de aprobadas (si quieres mostrar todas vs aprobadas)
    total_todas = Opinion.objects.count()
    porcentaje_aprobadas = (total_opiniones / total_todas * 100) if total_todas > 0 else 0
    
    # Casas del usuario para el formulario (si está autenticado)
    casas_usuario = []
    if request.user.is_authenticated:
        # Aquí debes implementar la lógica para obtener las casas que el usuario ha rentado
        # Esto es un ejemplo - ajusta según tu modelo de Reservas
        casas_usuario = Casa.objects.all()  # Reemplaza con tu lógica real
    
    context = {
        'opiniones': opiniones_aprobadas,
        'promedio_calificacion': round(promedio_calificacion, 1) if promedio_calificacion else None,
        'total_opiniones': total_opiniones,
        'porcentaje_aprobadas': round(porcentaje_aprobadas, 1),
        'opiniones_ultimo_mes': Opinion.objects.filter(
            aprobada=True,
            fecha_creacion__month=timezone.now().month
        ).count(),
        'casas_usuario': casas_usuario,
    }
    
    return render(request, 'inicio/opiniones.html', context)

def lista_promociones(request):
    hoy = timezone.now().date()
    promociones = Promocion.objects.filter(fecha_fin__gte=hoy)
    return render(request, 'inicio/lista_promociones.html', {'promociones': promociones})

# Crear promoción (solo admin)
@login_required
@user_passes_test(es_administrador)
def crear_promocion(request):
    if request.method == 'POST':
        form = PromocionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promoción creada correctamente!')
            return redirect('casas:lista_promociones')
    else:
        form = PromocionForm()
    return render(request, 'inicio/crear_promocion.html', {'form': form})

