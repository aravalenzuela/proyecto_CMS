from django.shortcuts import render, redirect

# Create your views here.

from Gestion_Contenido.models import PlantillaUsuario


# En views.py
from .models import PlantillaUsuario

from django.http import HttpResponse  # Asegúrate de importar HttpResponse


# Asegúrate de importar los modelos y formularios necesarios aquí


from .models import Plantilla, ContenidoEditable
from .forms import ContenidoEditableForm,PlantillaMultimediaForm  # Asegúrate de importar los formularios necesarios

from django.http import HttpResponseRedirect


from .forms import SeleccionarPlantillaForm, ConfiguracionSitioForm  # Asegúrate de importar ConfiguracionSitioForm


from .forms import ReporteForm



from .forms import ReporteForm
import json
from Seguridad.models import Categoria, Subcategoria

from Seguridad.models import Contenido

import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.http import JsonResponse

    
from Seguridad.models import TipoDeContenido, Contenido  # Ajusta según tus modelos
# Importa las bibliotecas necesarias
from django.http import HttpResponseBadRequest

# Importar el modelo Subcategoria
from Seguridad.models import Subcategoria

# Asegúrate de importar lo necesario al principio del archivo


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





def reportes_view(request):
    form = ReporteForm()

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)
        
        if informe_seleccionado == 'subcategorias_por_categorias':
            categorias = Categoria.objects.all()
            datos_informe = []
            
            for categoria in categorias:
                subcategorias_count = Subcategoria.objects.filter(categoria_relacionada=categoria).count()
                datos_informe.append({'categoria': categoria.nombre, 'cantidad_subcategorias': subcategorias_count})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)
                
                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                plt.pie(df['cantidad_subcategorias'], labels=df['categoria'], autopct='%1.1f%%', startangle=90)
                plt.title('Proporción de Subcategorías por Categoría')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})
     
    return render(request, 'reportes.html', {'form': form})


def reporte_tipos_plantillas(request):
    form = ReporteForm()  # Agrega el formulario

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)
        
        
        if informe_seleccionado == 'tipo_plantillas_por_plantillas':
            # Obtener la información sobre la proporción de tipos de plantillas
            total_plantillas = Plantilla.objects.count()
            blog_plantillas = Plantilla.objects.filter(tipo='blog').count()
            multimedia_plantillas = Plantilla.objects.filter(tipo='multimedia').count()
            

            # Crear un diccionario con los datos
            datos_informe = {
                'Blog': blog_plantillas,
                'Multimedia': multimedia_plantillas,
            }

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(list(datos_informe.items()), columns=['Tipo de Plantilla', 'Cantidad'])
                
                # Generar el gráfico de torta
                plt.figure(figsize=(8, 8))
                plt.pie(df['Cantidad'], labels=df['Tipo de Plantilla'], autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightskyblue'])
                plt.title('Proporción de Tipos de Plantillas')
                plt.axis('equal')  # Asegura que el gráfico de torta sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud AJAX o el informe no coincide, convierte datos a formato JSON para el gráfico
    return render(request, 'reportes.html', {'form': form})







def reporte_estados_tablero(request):
    form = ReporteForm()

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)
        
        if informe_seleccionado == 'estados_en_tablero':
            # Obtén los datos necesarios para el informe
            estados = ['Borrador', 'En Revisión', 'Rechazado', 'Publicado', 'Inactivo']
            datos_informe = []
            
            for estado in estados:
                contenidos_count = Contenido.objects.filter(estado=estado).count()
                datos_informe.append({'estado': estado, 'cantidad_contenidos': contenidos_count})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                plt.pie(df['cantidad_contenidos'], labels=df['estado'], autopct='%1.1f%%', startangle=90)
                plt.title('Proporción de Contenidos por Estado en el Tablero Kanban')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'reportes.html', {'form': form})



def reporte_tipo_contenido(request):
    form = ReporteForm()  # Ajusta el formulario según tus necesidades

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)
        
        if informe_seleccionado == 'contenido_por_tipos_de_contenidos':
            # Obtén los datos necesarios para el informe
            tipos_contenido = TipoDeContenido.objects.all()
            total_contenidos = Contenido.objects.count()
            datos_informe = []

            for tipo in tipos_contenido:
                contenidos_count = Contenido.objects.filter(tipo=tipo).count()
                porcentaje = (contenidos_count / total_contenidos) * 100 if total_contenidos > 0 else 0
                datos_informe.append({'tipo': tipo.nombre, 'porcentaje': porcentaje})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)
                
                # Generar el gráfico de torta
                plt.figure(figsize=(8, 8))
                plt.pie(df['porcentaje'], labels=df['tipo'], autopct='%1.1f%%', startangle=90)
                plt.title('Proporción de Contenido por Tipo de Contenido')
                plt.axis('equal')  # Asegura que el gráfico de torta sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'reportes.html', {'form': form})




def reporte_estados_categorias(request):
    form = ReporteForm()

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)

        if informe_seleccionado == 'estados_de_categorias':
            # Obtén los datos necesarios para el informe
            estados = ['Activo', 'Inactivo']
            datos_informe = []

            for estado in estados:
                categorias_count = Categoria.objects.filter(activo=(estado == 'Activo')).count()
                datos_informe.append({'estado': estado, 'cantidad_categorias': categorias_count})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                plt.pie(df['cantidad_categorias'], labels=df['estado'], autopct='%1.1f%%', startangle=90)
                plt.title('Proporción de Categorías por Estado')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'reportes.html', {'form': form})



def reporte_proporcion_plantillas(request):
    form = ReporteForm()

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)

        if informe_seleccionado == 'proporcion_plantillas':
            # Obtén los datos necesarios para el informe
            plantillas = Plantilla.objects.all()
            total_plantillas = plantillas.count()
            datos_informe = []

            for plantilla in plantillas:
                contenido_count = Contenido.objects.filter(plantilla=plantilla).count()
                porcentaje = (contenido_count / total_plantillas) * 100 if total_plantillas > 0 else 0
                datos_informe.append({'plantilla': plantilla.nombre, 'porcentaje': porcentaje})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de torta
                plt.figure(figsize=(8, 8))
                plt.pie(df['porcentaje'], labels=df['plantilla'], autopct='%1.1f%%', startangle=90)
                plt.title('Proporción de Plantillas en Tipos de Contenido')
                plt.axis('equal')  # Asegura que el gráfico de torta sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'reportes.html', {'form': form})





def generar_reporte(request):
    if request.method == 'POST':
        informe_seleccionado = request.POST.get('informe', None)
        if informe_seleccionado == 'subcategorias_por_categorias':
            
            return reportes_view(request)
        elif informe_seleccionado == 'tipo_plantillas_por_plantillas':
            return reporte_tipos_plantillas(request)
        elif informe_seleccionado == 'estados_en_tablero':
            
            return reporte_estados_tablero(request)
        
        elif informe_seleccionado == 'contenido_por_tipos_de_contenidos':
            return reporte_tipo_contenido(request)
        
        elif informe_seleccionado == 'estados_de_categorias':
            return reporte_estados_categorias(request)
        
        elif informe_seleccionado == 'proporcion_plantillas':
            return reporte_proporcion_plantillas(request)

    return HttpResponseBadRequest("Bad Request: Informe no válido.")

