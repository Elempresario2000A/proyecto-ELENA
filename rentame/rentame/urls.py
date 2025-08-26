# rentame/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from principal import views as inicio_views  # Importar vistas de la app inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('', include('principal.urls')),  # Si tienes app principal
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)