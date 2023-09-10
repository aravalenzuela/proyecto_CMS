from django import forms
<<<<<<< HEAD
from .models import Categoria, Rol
=======
from .models import Permiso

class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())
from .models import Categoria
>>>>>>> 45f777ebaded6472e1f5c8a667a4a4d7a6fd5ede

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']