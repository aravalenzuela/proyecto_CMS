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
                subcategorias = Subcategoria.objects.filter(categoria_relacionada=categoria)
                subcategorias_count = subcategorias.count()
                subcategorias_list = [subcategoria.nombre for subcategoria in subcategorias]
                datos_informe.append({'categoria': categoria.nombre, 'subcategorias': subcategorias_list, 'cantidad_subcategorias': subcategorias_count})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)
                
                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                patches, texts, autotexts = plt.pie(
                    df['cantidad_subcategorias'],
                    labels=df['categoria'],
                    autopct='%1.1f%%',
                    startangle=90,
                    textprops=dict(size=14),  # Ajusta el tamaño de la fuente
                
                )
                
                plt.title('Proporción de Subcategorías por Categoría', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Crear una cadena de detalles del informe para el HTML
                
                detalles_html = "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"
                for item in datos_informe:
                    detalles_html += "<div style='font-size: 14px;'>"  # Ajusta el tamaño de fuente según tus preferencias
                    detalles_html += f"<p><strong>Categoria</strong> : {item['categoria']} </p>"
                    
                    # Verificar si la cantidad de subcategorías es mayor a 4
                    if item['cantidad_subcategorias'] > 0:
                        if item['cantidad_subcategorias'] > 5:
                            detalles_html += "<p><strong>Subcategorias Relacionada</strong>:</p>"
                            for i, subcategoria in enumerate(item['subcategorias'], 1):
                                detalles_html += f"{subcategoria}, "
                                # Hacer el salto de línea después de cada múltiplo de 4
                                if i % 5 == 0:
                                    detalles_html += "<br>"
                        else:
                            detalles_html += f"<p><strong>Subcategorias Relacionada</strong>: {', '.join(item['subcategorias'])}</p>"
                    else:
                        detalles_html += "<p><strong>Subcategorias Relacionada</strong>: Ninguna</p>"

                    
                    detalles_html += f"<p><strong>Total de Subcategorias</strong> = {item['cantidad_subcategorias']}</p>"
                    detalles_html += "</div>"

                    # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"

                # Agrega la descripción debajo del gráfico
                descripcion_html = """
                    <p style='font-size: 14px;'><strong>Descripcion :</strong>  El reporte ofrece una descripción detallada sobre cada categoría y sus respectivas subcategorías.<br>
                    Además de una representación visual intuitiva de cómo las subcategorías están distribuidas entre diferentes categorías</p>
                """

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

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
            tipos_de_plantillas = Plantilla.TIPO_CHOICES
            datos_informe = {}
            
            for tipo, _ in tipos_de_plantillas:
                plantillas = Plantilla.objects.filter(tipo=tipo)
                plantillas_list = [plantilla.nombre for plantilla in plantillas]
                cantidad_plantillas = len(plantillas_list)
                
                # Convertir tipo a mayúsculas
                tipo_mayusculas = tipo.capitalize()
                
                datos_informe[tipo_mayusculas] = {
                    'plantillas': plantillas_list,
                    'cantidad_plantillas': cantidad_plantillas
                }

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame([(k, v['cantidad_plantillas']) for k, v in datos_informe.items()], columns=['Tipo de Plantilla', 'Cantidad'])
                
                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                patches, texts, autotexts = plt.pie(
                    df['Cantidad'],
                    labels=df['Tipo de Plantilla'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=['red', 'yellow'],
                    textprops=dict(size=16),
                    pctdistance=0.5
                )
                
                plt.title('Proporción de Plantillas por Tipos de Plantillas', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Crear una cadena de detalles del informe para el HTML
                detalles_html = "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"
                
                for tipo, detalles in datos_informe.items():
                    
                    detalles_html += f"<p>Plantillas del Tipo <strong>{tipo}</strong>:  {', '.join(detalles['plantillas'])}</p>"
                    detalles_html += f"<p>Cantidad de Plantillas Tipo <strong>{tipo}</strong> =  {detalles['cantidad_plantillas']}</p>"
                    

                    # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"

                # Agrega la descripción debajo del gráfico
                descripcion_html = """
                    <p style='font-size: 14px;'><strong>Descripcion :</strong> El informe presenta la proporción de plantillas según su tipo.<br>
                    Muestra cómo se distribuyen las plantillas entre los tipos 'Blog' y 'Multimedia' en términos de cantidad.</p>
                """

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

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
                contenidos = Contenido.objects.filter(estado=estado)
                contenidos_list = [contenido.titulo for contenido in contenidos]
                datos_informe.append({'estado': estado, 'contenidos': contenidos_list, 'cantidad_contenidos': contenidos.count()})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))

                patches, texts, autotexts = plt.pie(
                    df['cantidad_contenidos'], 
                    labels=df['estado'], 
                    autopct='%1.1f%%', 
                    startangle=90,
                    textprops=dict(size=16),
      
                )


                plt.title('Proporción de Contenidos por Estado en el Tablero Kanban', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Crear una cadena de detalles del informe para el HTML
                detalles_html = ""
                detalles_html += "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"
                for item in datos_informe:
                    detalles_html += "<div style='font-size: 14px;'>"  # Ajusta el tamaño de fuente según tus preferencias
                    
                    # Verificar si la cantidad de contenidos es mayor a 5
                    if len(item["contenidos"]) > 0:

                        if len(item["contenidos"]) > 5:
                            detalles_html += f'<p><strong> Contenidos en el Estado  "{item["estado"]}" : </strong></p>'
                            for i, contenido in enumerate(item["contenidos"], 1):
                                detalles_html += f"{contenido}, "
                                # Hacer el salto de línea después de cada múltiplo de 5
                                if i % 5 == 0:
                                    detalles_html += "<br>"
                        else:
                            detalles_html += f'<p><strong> Contenidos en el Estado  "{item["estado"]}" : </strong> {", ".join(item["contenidos"])}</p>'

                    else:
                        detalles_html += f'<p><strong> Contenidos en el Estado  "{item["estado"]}" : </strong> Ninguno</p>'
                    
                    detalles_html += f"<p><strong> Total en {item['estado']}</strong>  = {item['cantidad_contenidos']}</p>"

                    # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"

                # Agrega la descripción debajo del gráfico
                descripcion_html = """
                    <p style='font-size: 14px;'><strong>Descripcion :</strong> Este reporte muestra la proporción de contenidos en diferentes estados en el tablero Kanban.<br>
                    Proporciona una visión general de cómo se distribuyen los contenidos en estados como : <br>
                    'Borrador', 'En Revisión', 'Rechazado', 'Publicado' e 'Inactivo'.</p>
                """


                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form})

    # Si no es una solicitud POST, simplemente renderiza el formulario
    return render(request, 'reportes.html', {'form': form})




def reporte_tipo_contenido(request):
    form = ReporteForm()

    if request.method == 'POST':
        form = ReporteForm(request.POST)
        informe_seleccionado = request.POST.get('informe', None)

        if informe_seleccionado == 'contenido_por_tipos_de_contenidos':
            # Obtén los datos necesarios para el informe
            tipos_contenido = TipoDeContenido.objects.all()
            total_contenidos = Contenido.objects.count()
            datos_informe = []

            for tipo in tipos_contenido:
                contenidos = Contenido.objects.filter(tipo=tipo)
                contenidos_list = [contenido.titulo for contenido in contenidos]
                datos_informe.append({'tipo': tipo.nombre, 'contenidos': contenidos_list, 'total_contenidos': contenidos.count()})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de torta
                plt.figure(figsize=(10, 6))

                patches, texts, autotexts = plt.pie(
                    df['total_contenidos'], 
                    labels=df['tipo'], 
                    autopct='%1.1f%%', 
                    startangle=90,
                    textprops=dict(size=14),  # Ajusta el tamaño de la fuente
                    pctdistance=0.5
                        
                )
                
                plt.title('Proporción de Contenido por Tipo de Contenido', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de torta sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Crear una cadena de detalles del informe para el HTML
                detalles_html = ""
                detalles_html += "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"
                for item in datos_informe:
                    detalles_html += "<div style='font-size: 12px;'>"  # Ajusta el tamaño de fuente según tus preferencias
                    detalles_html += f"<p><strong>Tipo de Contenido : </strong>{item['tipo']}</strong> </p>"
                    
                     # Verificar si la cantidad de contenidos asociados es mayor a 4
                    if len(item['contenidos']) > 0:
                        if len(item['contenidos']) > 4:
                            detalles_html += "<p><strong>Contenido asociado :</strong></p>"
                            for i, contenido in enumerate(item['contenidos'], 1):
                                detalles_html += f"{contenido}"
                                # Hacer el salto de línea después de cada múltiplo de 4, pero no en la última iteración
                                if i % 4 == 0 and i < len(item['contenidos']):
                                    detalles_html += "<br>"
                                    # Agregar coma y espacio si no es la última iteración
                                if i < len(item['contenidos']):
                                    detalles_html += ", "
                        else:
                            detalles_html += f"<p><strong>Contenido asociado :</strong> {', '.join(item['contenidos'])}</p>"

                    else:
                        detalles_html += "<p><strong>Contenido asociado :</strong> Ninguno</p>"

                    detalles_html += f"<p><strong>Total de Contenidos = </strong> {item['total_contenidos']}</p>"

                     # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"

                # Agrega la descripción debajo del gráfico
                descripcion_html = """
                    <div style='margin-top: 20px;'>
                        <p style='font-size: 14px;'><strong>Descripcion :</strong> Este reporte muestra la proporción de contenido por tipo de contenido.<br>
                        <p style='font-size: 14px;'>Y gráfico representa el porcentaje de contenido para cada tipo de contenido.</p>
                    </div>
                """

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

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
                categorias = Categoria.objects.filter(activo=(estado == 'Activo'))
                categorias_list = [categoria.nombre for categoria in categorias]
                datos_informe.append({'estado': estado, 'categorias': categorias_list, 'cantidad_categorias': categorias.count()})

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de pastel
                plt.figure(figsize=(10, 6))
                
                patches, texts, autotexts = plt.pie(
                    df['cantidad_categorias'], 
                    labels=df['estado'], 
                    autopct='%1.1f%%', 
                    startangle=90,
                    colors=['green', 'yellow'],
                    textprops=dict(size=16),
                    pctdistance=0.5
                )
                
                plt.title('Proporción de Categorías por Estado', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de pastel sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'

                # Crear una cadena de detalles del informe para el HTML
                detalles_html = ""
                detalles_html += "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"
                for item in datos_informe:
                    detalles_html += "<div style='font-size: 14px;'>"  # Ajusta el tamaño de fuente según tus preferencias
                    
                    
                    # Verificar si la cantidad de categorías es mayor a 5
                    if item['cantidad_categorias'] > 0:
                        if len(item['categorias']) > 5:
                            detalles_html += f"<p><strong>Categorías en el estado \"{item['estado']}\" :</strong></p>"
                            for i, categoria in enumerate(item['categorias'], 1):
                                detalles_html += f"{categoria}, "
                                
                            detalles_html = detalles_html.rstrip(', ')  # Eliminar la última coma y espacio
                        else:
                            detalles_html += f"<p><strong>Categorías en el estado \"{item['estado']}\" :</strong> {', '.join(item['categorias'])}</p>"

                    else:
                        detalles_html += f"<p><strong>Categorías en el estado \"{item['estado']}\" :</strong> Ninguna</p>"


                    detalles_html += f"<p><strong>Cantidad Total {item['estado']}</strong> = {item['cantidad_categorias']}</p>"
                    
                    # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"

                # Agrega la descripción debajo del gráfico
                descripcion_html = """
                    <p style='font-size: 14px;'><strong>Descripcion :</strong> Este reporte muestra la proporción de categorías en diferentes estados, como 'Activo' e 'Inactivo'.<br>
                    Proporciona información sobre la cantidad de categorías activas e inactivas en el sistema.</p>
                """


                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

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

            detalles_html = ""  # Inicializa la cadena de detalles
            detalles_html += "<div style='text-align: center; font-weight: bold;'>Detalles del Reporte</div>"

            for plantilla in plantillas:
                contenido_count = Contenido.objects.filter(plantilla=plantilla).count()
                porcentaje = (contenido_count / total_plantillas) * 100 if total_plantillas > 0 else 0
                datos_informe.append({'plantilla': plantilla.nombre, 'porcentaje': porcentaje})

                # Agrega detalles para cada tipo de contenido y sus plantillas correspondientes
                plantillas_tipo_contenido = Contenido.objects.filter(plantilla=plantilla)
                
                if plantillas_tipo_contenido.exists():
                    detalles_html += "<div style='font-size: 14px;'>"  # Ajusta el tamaño de fuente según tus preferencias


                    # Obtener la lista de tipos de contenido
                    tipos_contenido = plantillas_tipo_contenido.values_list('titulo', flat=True)

                    # Verificar si la cantidad de tipos de contenido es mayor a 5
                    if len(tipos_contenido) > 5:
                        detalles_html += f"<p><strong>Tipos de Contenido en {plantilla.nombre} :</strong></p>"
                        for i, tipo_contenido in enumerate(tipos_contenido, 1):
                            detalles_html += f"{tipo_contenido}, "
                            # Hacer el salto de línea después de cada múltiplo de 5, pero no en la última iteración
                            if i % 5 == 0 and i < len(tipos_contenido):
                                detalles_html += "<br>"
                        detalles_html = detalles_html.rstrip(', ')  # Eliminar la última coma y espacio
                    else:
                        detalles_html += f"<p><strong>Tipos de Contenido en {plantilla.nombre} :</strong> {', '.join(tipos_contenido)}</p>"


                    detalles_html += f"<p><strong> Total de Tipos de Contenido  = </strong> {plantillas_tipo_contenido.count()}</p>"

                    # Agregar un espacio entre iteraciones
                    detalles_html += "<br>"


            # Agrega la descripción debajo del gráfico
            descripcion_html = """
                <p style='font-size: 14px;'><strong>Descripcion :</strong> Este reporte presenta la proporción de tipos de contenido por plantillas.<br>
                Muestra cómo se distribuyen los tipos de contenido en relación con las plantillas existentes en el sistema.</p>
            """

            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve los datos como respuesta JSON
                df = pd.DataFrame(datos_informe)

                # Generar el gráfico de torta
                plt.figure(figsize=(10, 6))

                patches, texts, autotexts = plt.pie(
                    df['porcentaje'], 
                    labels=df['plantilla'], 
                    autopct='%1.1f%%', 
                    startangle=90,
                    textprops=dict(size=14),
                    pctdistance=0.5
                )
                
                plt.title('Cantidad de Tipos de Contenido por Plantillas', fontsize=18, fontweight='bold', color='#3366cc')
                plt.axis('equal')  # Asegura que el gráfico de torta sea un círculo.

                # Guardar el gráfico en BytesIO para mostrarlo en el HTML
                img_data = BytesIO()
                plt.savefig(img_data, format='png')
                img_data.seek(0)
                img_base64 = base64.b64encode(img_data.read()).decode()
                img_src = f'data:image/png;base64,{img_base64}'
                

                # Devuelve los datos como respuesta JSON
                return JsonResponse({'datos': datos_informe, 'img_src': img_src, 'informe_detalles': detalles_html, 'informe_detalles_adicionales': descripcion_html})

            # Si no es una solicitud AJAX, convierte datos a formato JSON para el gráfico
            return render(request, 'reportes.html', {'form': form, 'informe_detalles': detalles_html})

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

