# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm
from .models import CustomUser # Asegúrate de importar tu modelo de reservas
from principal.models import Reserva

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('usuarios:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuarios/registrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.username}!')
                return redirect('casas:Principal')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('casas:Principal')

# VISTAS DE DASHBOARD Y PERFIL
@login_required
def user_dashboard(request):
    """Dashboard principal del usuario"""
    user = request.user
    reservas_recientes = Reserva.objects.filter(usuario=user).order_by('-fecha_creacion')[:5]
    total_reservas = Reserva.objects.filter(usuario=user).count()
    
    context = {
        'user': user,
        'reservas_recientes': reservas_recientes,
        'total_reservas': total_reservas,
    }
    return render(request, 'usuarios/dashboard/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Dashboard de administrador"""
    if not request.user.is_admin():
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('usuarios:user_dashboard')
    
    # Estadísticas para admin
    total_usuarios = CustomUser.objects.count()
    total_reservas = Reserva.objects.count()
    reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
    
    context = {
        'total_usuarios': total_usuarios,
        'total_reservas': total_reservas,
        'reservas_pendientes': reservas_pendientes,
    }
    return render(request, 'usuarios/dashboard/admin_dashboard.html', context)

@login_required
def moderator_dashboard(request):
    """Dashboard de moderador"""
    if not request.user.is_moderator() and not request.user.is_admin():
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('usuarios:user_dashboard')
    
    reservas_recientes = Reserva.objects.all().order_by('-fecha_creacion')[:10]
    
    context = {
        'reservas_recientes': reservas_recientes,
    }
    return render(request, 'usuarios/dashboard/moderator_dashboard.html', context)

@login_required
def user_profile(request):
    """Edición del perfil de usuario"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('usuarios:user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'usuarios/profile/user_profile.html', {'form': form})

@login_required
def my_reservations(request):
    """Lista de reservas del usuario"""
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context = {
        'reservas': reservas,
    }
    return render(request, 'usuarios/reservations/my_reservations.html', context)

@login_required
def reservation_detail(request, reservation_id):
    """Detalle de una reserva específica"""
    reserva = get_object_or_404(Reserva, id=reservation_id, usuario=request.user)
    
    context = {
        'reserva': reserva,
    }
    return render(request, 'usuarios/reservations/reservation_detail.html', context)