from django.urls import path
from . import views

app_name = 'casas'

urlpatterns = [
    path('opiniones/', views.opiniones, name='opiniones'),
    path('', views.Principal, name='Principal'),
    path('listas/', views.lista_casas, name='lista_casas'),
    path('casa/<int:casa_id>/', views.detalle_casa, name='detalle_casa'),
    path('opiniones/', views.Opiniones, name='Opiniones'),
    path('contacto/', views.Opiniones, name='Contacto'),
    path('crear/', views.crear_casa, name='crear_casa'),
    path('editar/<int:casa_id>/', views.editar_casa, name='editar_casa'),
    path('eliminar/<int:casa_id>/', views.eliminar_casa, name='eliminar_casa'),
        # URLs para opiniones
    path('casa/<int:casa_id>/opinion/crear/', views.crear_opinion, name='crear_opinion'),
    path('mis-opiniones/', views.mis_opiniones, name='mis_opiniones'),
    path('opinion/<int:opinion_id>/editar/', views.editar_opinion, name='editar_opinion'),
    path('opinion/<int:opinion_id>/eliminar/', views.eliminar_opinion, name='eliminar_opinion'),
    
    # URLs para moderación (admin only)
    path('moderar-opiniones/', views.moderar_opiniones, name='moderar_opiniones'),
    path('opinion/<int:opinion_id>/aprobar/', views.aprobar_opinion, name='aprobar_opinion'),
    path('opinion/<int:opinion_id>/rechazar/', views.rechazar_opinion, name='rechazar_opinion'),

    path('promociones/', views.lista_promociones, name='lista_promociones'),
    path('promociones/crear/', views.crear_promocion, name='crear_promocion')
]