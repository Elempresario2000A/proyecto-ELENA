from django import forms
from .models import Casa, ImagenCasa, Opinion, Promocion

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = [
            'nombre', 'descripcion', 'ubicacion', 'precio_noche',
            'capacidad', 'habitaciones', 'banos', 'imagen_principal',
            'estado', 'destacada'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'precio_noche': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ImagenCasaForm(forms.ModelForm):
    class Meta:
        model = ImagenCasa
        fields = ['imagen', 'descripcion']

class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={
                'min': 1, 
                'max': 5, 
                'class': 'form-control',
                'placeholder': 'Calificación (1-5)'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu experiencia con esta casa...'
            })
        }
        labels = {
            'calificacion': 'Calificación',
            'comentario': 'Comentario'
        }        

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['casa', 'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'imagen']