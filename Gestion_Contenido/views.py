from django.shortcuts import render, redirect

# Create your views here.

from Gestion_Contenido.models import PlantillaUsuario
from Seguridad.models import Notificacion

# En views.py
from .models import PlantillaUsuario

from django.http import HttpResponse  # Asegúrate de importar HttpResponse


# Asegúrate de importar los modelos y formularios necesarios aquí


from .models import Plantilla, ContenidoEditable
from .forms import ContenidoEditableForm,PlantillaMultimediaForm  # Asegúrate de importar los formularios necesarios

from django.http import HttpResponseRedirect


from .forms import SeleccionarPlantillaForm, ConfiguracionSitioForm  # Asegúrate de importar ConfiguracionSitioForm

from django.shortcuts import render, redirect


def listar_plantillas(request):

    """
    Lista todas las plantillas disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de plantillas.
    """
        
    plantillas = Plantilla.objects.all()
    
    return render(request, 'listar_plantillas.html', {'plantillas': plantillas})




def seleccionar_plantilla(request):

    """
    Permite al usuario seleccionar una plantilla para su perfil.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de selección de plantilla o guarda la selección en la sesión.
    """
        
    configuracion_form = ConfiguracionSitioForm() 
    usuario_actual = request.user
    
    if request.method == 'POST':
        form = SeleccionarPlantillaForm(request.POST)
        if form.is_valid():
            plantilla_seleccionada = form.cleaned_data['plantilla']

            # Guarda la plantilla seleccionada en la sesión
            request.session['plantilla_seleccionada_id'] = plantilla_seleccionada.id

            return HttpResponseRedirect('/seleccionar_plantilla')  # Redirige para actualizar la vista
    else:
        form = SeleccionarPlantillaForm()

    # Obtén la última plantilla seleccionada del usuario actual desde la sesión
    plantilla_seleccionada_id = request.session.get('plantilla_seleccionada_id')
    plantilla_seleccionada = None

    if plantilla_seleccionada_id is not None:
        try:
            plantilla_seleccionada = Plantilla.objects.get(id=plantilla_seleccionada_id)
        except Plantilla.DoesNotExist:
            pass

    return render(request, 'seleccionar_plantilla.html', {
        'form': form,
        'configuracion_form': configuracion_form,
        'plantilla_seleccionada': plantilla_seleccionada,
    })



def profile_view(request):

    """
    Muestra el perfil del usuario, incluyendo la plantilla seleccionada y el contenido editable.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de perfil del usuario.
    """
        
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

    # Obtener notificaciones del usuario
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)

    # Pasar notificaciones al contexto
    context['notificaciones'] = notificaciones

    return render(request, 'profile.html', context)



def editar_plantilla(request):

    """
    Permite al usuario editar la plantilla seleccionada, incluyendo la carga de imágenes.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de edición de la plantilla o guarda los cambios en la base de datos.
    """
        
    # Obtener el usuario actual y su plantilla seleccionada desde la sesión
    usuario_actual = request.user

    # Obtener la plantilla seleccionada a través de la sesión
    plantilla_seleccionada_id = request.session.get('plantilla_seleccionada_id')
    plantilla_seleccionada = None

    if plantilla_seleccionada_id is not None:
        try:
            plantilla_seleccionada = Plantilla.objects.get(id=plantilla_seleccionada_id)
        except Plantilla.DoesNotExist:
            pass

    if request.method == 'POST':
        # Utiliza PlantillaMultimediaForm para permitir cargar imágenes
        contenido_editable_form = PlantillaMultimediaForm(request.POST, request.FILES, instance=plantilla_seleccionada)
        if contenido_editable_form.is_valid():
            contenido_nuevo = contenido_editable_form.cleaned_data['contenidoDePlantilla']

            # Guardar los cambios en la base de datos
            contenido_editable_form.save()
    else:
        # Utiliza PlantillaMultimediaForm para permitir cargar imágenes
        contenido_editable_form = PlantillaMultimediaForm(instance=plantilla_seleccionada)

    contenido_editable = plantilla_seleccionada.contenido_editable if plantilla_seleccionada else ""

    # Obtener todos los campos de la plantilla para mostrarlos
    plantilla_data = {
        'nombre': plantilla_seleccionada.nombre if plantilla_seleccionada else "",
        'tipo': plantilla_seleccionada.tipo if plantilla_seleccionada else "",
        'contenidoDePlantilla': plantilla_seleccionada.contenidoDePlantilla if plantilla_seleccionada else "",
    }

    return render(request, 'editar_plantilla.html', {
        'form': contenido_editable_form,
        'contenido_editable': contenido_editable,
        'plantilla_seleccionada': plantilla_data,  # Mostrar los detalles de la plantilla
    })



def ver_plantilla(request):

    """
    Muestra los detalles de la plantilla seleccionada por el usuario.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de detalles de la plantilla.
    """
        
    # Obtener el usuario actual y su plantilla seleccionada desde la sesión
    usuario_actual = request.user

    # Obtener la plantilla seleccionada a través de la sesión
    plantilla_seleccionada_id = request.session.get('plantilla_seleccionada_id')
    plantilla_seleccionada = None

    if plantilla_seleccionada_id is not None:
        try:
            plantilla_seleccionada = Plantilla.objects.get(id=plantilla_seleccionada_id)
        except Plantilla.DoesNotExist:
            pass

    contenido_editable = plantilla_seleccionada.contenido_editable if plantilla_seleccionada else ""

    # Obtener todos los campos de la plantilla para mostrarlos
    plantilla_data = {
        'nombre': plantilla_seleccionada.nombre if plantilla_seleccionada else "",
        'tipo': plantilla_seleccionada.tipo if plantilla_seleccionada else "",
        'contenidoDePlantilla': plantilla_seleccionada.contenidoDePlantilla if plantilla_seleccionada else "",
    }

    return render(request, 'ver_plantilla.html', {
        'contenido_editable': contenido_editable,
        'plantilla_seleccionada': plantilla_data,
        'imagen': plantilla_seleccionada.imagen,  # Pasa la imagen a la plantilla
    })