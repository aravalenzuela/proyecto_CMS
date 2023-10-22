from django import forms
from .models import Categoria, Rol, Permiso, Subcategoria, Usuario
from django.contrib.auth.models import User

class AsignarRolForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol']

     # Opcional: Si quieres listar a todos los usuarios
    user = forms.ModelChoiceField(queryset=User.objects.all())
        
class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Usamos casillas de verificación para seleccionar múltiples permisos
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']



class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria_relacionada']  # Asegúrate de que estos campos coincidan con los de tu modelo



#class SeleccionarPlantillaForm(forms.Form):
#    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())
