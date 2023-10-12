from django.shortcuts import render, redirect

# Create your views here.

from Gestion_Contenido.models import PlantillaUsuario


# En views.py
from .models import PlantillaUsuario

from django.http import HttpResponse  # Asegúrate de importar HttpResponse


# Asegúrate de importar los modelos y formularios necesarios aquí


from .models import Plantilla, ContenidoEditable
from .forms import SeleccionarPlantillaForm, ContenidoEditableForm  # Asegúrate de importar los formularios necesarios

from django.http import HttpResponseRedirect


from .forms import SeleccionarPlantillaForm, ConfiguracionSitioForm  # Asegúrate de importar ConfiguracionSitioForm




def listar_plantillas(request):
    plantillas = Plantilla.objects.all()
    
    return render(request, 'listar_plantillas.html', {'plantillas': plantillas})


# En views.py
from django.shortcuts import render, redirect

# Resto del código...

def seleccionar_plantilla(request):
    configuracion_form = ConfiguracionSitioForm() 
     
    if request.method == 'POST':
        form = SeleccionarPlantillaForm(request.POST)
        if form.is_valid():
            plantilla_seleccionada = form.cleaned_data['plantilla']
            usuario_actual = request.user

            # Resto del código...

            return render(request, 'seleccionar_plantilla.html', {
                'form': form,
                'configuracion_form': configuracion_form,
                'plantilla_seleccionada': plantilla_seleccionada,  # Agrega esta línea
            })
    else:
        form = SeleccionarPlantillaForm()
        

    return render(request, 'seleccionar_plantilla.html', {
        'form': form,
        'configuracion_form': configuracion_form,
    })



def profile_view(request):
    context = {}  # Define el contexto como un diccionario vacío

    # Agrega aquí tu lógica existente para obtener información del usuario

    try:
        plantilla_usuario = PlantillaUsuario.objects.get(usuario=request.user)
        context['plantilla_usuario'] = plantilla_usuario

        if plantilla_usuario.plantillas.count() > 0:
            # Obtén el contenido editable de la primera plantilla asociada al usuario
            contenido_editable = plantilla_usuario.plantillas.first().contenido_editable
            context['contenido_editable'] = contenido_editable
        else:
            context['contenido_editable'] = ""
    except PlantillaUsuario.DoesNotExist:
        context['plantilla_usuario'] = None
        context['contenido_editable'] = ""

    return render(request, 'profile.html', context)



def editar_plantilla(request):
    # Obtener el usuario actual y su plantilla seleccionada
    usuario_actual = request.user
    plantilla_usuario, created = PlantillaUsuario.objects.get_or_create(usuario=usuario_actual)
    plantilla_seleccionada = plantilla_usuario.plantillas.first()

    if request.method == 'POST':
        contenido_editable_form = ContenidoEditableForm(request.POST)
        if contenido_editable_form.is_valid():
            contenido_nuevo = contenido_editable_form.cleaned_data['contenido']

            # Actualizar el contenido editable de la plantilla seleccionada
            if plantilla_seleccionada:
                plantilla_seleccionada.contenido_editable = contenido_nuevo
                plantilla_seleccionada.save()

    else:
        contenido_editable_form = ContenidoEditableForm()

    contenido_editable = plantilla_seleccionada.contenido_editable if plantilla_seleccionada else ""

    # Obtener todos los campos de la plantilla para mostrarlos
    plantilla_data = {
        'nombre': plantilla_seleccionada.nombre,
        'tipo': plantilla_seleccionada.tipo,
        'contenido': plantilla_seleccionada.contenido,
    }

    return render(request, 'editar_plantilla.html', {
        'form': contenido_editable_form,
        'contenido_editable': contenido_editable,
        'plantilla_seleccionada': plantilla_data,  # Mostrar los detalles de la plantilla
    })
