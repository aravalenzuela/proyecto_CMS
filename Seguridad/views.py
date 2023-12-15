from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.views import get_gravatar_url
from .models import Permiso, Usuario , Categoria, Rol , Contenido, TipoDeContenido, Subcategoria, Like, Comentario, RespuestaComentario, Compartido, Notificacion
from django.contrib import messages
from .forms import CategoriaForm, RolForm, CrearContenidoForm, AsignarRolForm, SubcategoriaForm, TipoDeContenidoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.http import require_http_methods

from Gestion_Contenido.models import Plantilla
from .forms import SubcategoriaForm
from django.urls import reverse

from core.views import get_gravatar_url
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

#from .models import Plantilla
#from .forms import SeleccionarPlantillaForm


from .forms import TipoDeContenidoForm

from .models import TipoDeContenido


#Codigos para la implementacion de los requerimientos
@login_required
def asignar_rol_a_usuario(request, usuario_id):
    """
    Asigna un rol a un usuario específico.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        usuario_id (int): ID del usuario al que se asignará el rol.
        
    Returns:
        HttpResponse: Renderiza la página de asignación de rol o redirige tras la asignación exitosa.
    """

    print("Entrando a la función asignar_rol_a_usuario")
    
    # Obtén la instancia del modelo Usuario basado en el usuario_id.
    seguridad_usuario = get_object_or_404(Usuario, user_id=usuario_id)
    print(f"Usuario obtenido: {seguridad_usuario.user.username}")

    if request.method == 'POST':
        print("Método POST detectado")
        
        # Ajusta el formulario para que use la instancia correcta
        form = AsignarRolForm(request.POST, instance=seguridad_usuario)
        
        if form.is_valid():
            print("Formulario válido")
            
            # Asegúrate de que estás obteniendo una instancia de Rol, no solo el ID.
            rol_seleccionado = form.cleaned_data['rol']
            seguridad_usuario.rol = rol_seleccionado
            
            print(f"Rol asignado al usuario: {seguridad_usuario.rol.nombre}")
            seguridad_usuario.save()


            # Recargar el usuario después de guardar el formulario
            # (Realmente no es necesario, puedes trabajar directamente con seguridad_usuario)
            
            if seguridad_usuario.rol:
                print(f"Rol asignado al usuario {seguridad_usuario.user.username}: {seguridad_usuario.rol.nombre}")
                
                # Crear notificación
                Notificacion.objects.create(
                usuario=seguridad_usuario.user,
                mensaje=f"Se te ha asignado el rol: '{seguridad_usuario.rol.nombre}'.",
            )
            else:
                print(f"Rol asignado al usuario {seguridad_usuario.user.username}: Sin Rol")
            
            messages.success(request, 'Roles asignados con éxito.')
            return redirect('profile_view')
        else:
            print(form.errors)
            messages.error(request, 'Ha ocurrido un error al asignar los roles.') # Usar messages.error para errores.
            print("Formulario no válido")
    else:
        form = AsignarRolForm(instance=seguridad_usuario)

    context = {
        'form': form,
        'usuario': seguridad_usuario.user  # Usar el usuario de la instancia de Usuario (seguridad_usuario)
    }
    return render(request, 'asignar_rol.html', context)



def crear_permiso(request):
    """
    Crea un nuevo permiso y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de permiso o redirige al perfil tras la creación exitosa.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        permiso = Permiso(nombre=nombre, descripcion=descripcion)
        permiso.save()
        return redirect('profile_view')  # Cambia esto al nombre real de la vista a la que deseas redirigir
    return render(request, 'crear_permiso.html')



def listar_permisos(request):
    """
    Lista todos los permisos disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de permisos.
    """
    permisos = Permiso.objects.all()
    return render(request, 'listar_permisos.html', {'permisos': permisos})



def list_users(request):
    """
    Lista todos los usuarios registrados en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de usuarios.
    """
    users = User.objects.all()

    # Asigna la URL Gravatar a cada usuario
    for user in users:
        user.gravatar_url = get_gravatar_url(user.email)
        
        # Accediendo a los campos de 'Usuario' desde el modelo 'User'
        if hasattr(user, 'usuario'):
            user_role = user.usuario.rol
        else:
            user_role = None  # o cualquier otro valor por defecto

        user.role_name = user_role.nombre if user_role else "Sin Rol Asignado"
        print(f"Roles for {user.username}: {user.role_name}")

    # ... Resto del código de la función
    return render(request, 'list_users.html', {'users': users})



def crear_usuario(request):
    """
    Crea un nuevo usuario y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de usuario o redirige tras la creación exitosa.
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Puedes agregar validaciones adicionales aquí
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('alguna_url_donde_redirigir')
        except:
            messages.error(request, 'Ha ocurrido un error al crear el usuario.')
        
    return render(request, 'crear_usuario.html')



def asignar_permiso(request, rol_id=None): 
    """
    Asigna permisos a un rol específico.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        rol_id (int, optional): ID del rol al que se asignarán los permisos. Defaults to None.
        
    Returns:
        HttpResponse: Renderiza la página de asignación de permisos o redirige tras la asignación exitosa.
    """
    rol = get_object_or_404(Rol, pk=rol_id) if rol_id else None
    
    if request.method == 'POST':
        form = AsignarRolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()  # Los permisos se guardarán automáticamente debido a ManyToMany
            mensajes_notificacion = [f"Has sido asignado al rol: {rol.nombre}" for rol in form.cleaned_data['permisos']]
            Notificacion.objects.bulk_create([Notificacion(usuario=User.user, mensaje=mensaje) for mensaje in mensajes_notificacion])
            
            messages.success(request, 'Permisos asignados con éxito.')
            return redirect('profile_view')
        else:
            print(form.errors)  # Agregar esta línea para imprimir los errores
            messages.error(request, 'Ha ocurrido un error al asignar los permisos.')
    else:
        form = AsignarRolForm(instance=rol)
    
    context = {
        'form': form
    }
    return render(request, 'asignar_permisos_a_rol.html', context)


def crear_categoria(request):
    """
    Crea una nueva categoría y la guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de categoría o redirige tras la creación exitosa.
    """

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            
            # Verificar si la categoría ya existe (insensible a mayúsculas y minúsculas)
            if Categoria.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, 'Esta categoría ya existe. Por favor, crea una nueva.')
            else:
                form.save()
                return redirect('profile_view')
        else:
            messages.error(request, 'No se puede crear la categoria. Hay dos posibilidades:')
            messages.error(request, '1) Debe completar correctamente todos los campos ')
            messages.error(request, '2) La categoria ya existe y debe crear una nueva')
    else:
        form = CategoriaForm()

    return render(request, 'crear_categoria.html', {'form': form})




def listar_categorias(request):
    """
    Lista todas las categorías disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})


@require_http_methods(["POST"])
def modificar_estado_categoria(request, categoria_id):

    """
    Vista que permite modificar el estado activo/inactivo de una categoría.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponseRedirect o JsonResponse: 
            - Si la categoría se encuentra y se modifica correctamente, se redirige a la página de listado de categorías con un parámetro de éxito.
            - Si la categoría no se encuentra, se devuelve una respuesta JSON con un mensaje de error y un código de estado 404.

    """


    try:
        categoria = Categoria.objects.get(pk=categoria_id)
        categoria.activo = not categoria.activo
        categoria.save()
        # Redirige de nuevo a la página de listado de categorías con un parámetro de éxito
        return redirect('listar_categorias')
    except Categoria.DoesNotExist:
        return JsonResponse({'mensaje': 'Categoría no encontrada'}, status=404)
    

def crear_rol(request):
    """
    Crea un nuevo rol y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de rol o redirige tras la creación exitosa.
    """
    print("Método de la petición:", request.method)
    print("La función crear_rol se ha llamado")
    if request.method == 'POST':
        print("Detectada petición POST")
        form = RolForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            form.save()
            return redirect('profile_view')  # Asegúrate de que esta vista existe y está definida en tu urls.py
    else:
        print("Petición no es POST, se asume GET y se muestra formulario")
        form = CategoriaForm()
    return render(request, 'crear_rol.html', {'form': form})



def listar_roles(request):
    """
    Lista todos los roles disponibles en la base de datos junto con sus permisos asociados.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de roles.
    """
    roles = Rol.objects.all().prefetch_related('permisos')
    return render(request, 'listar_roles.html', {'roles': roles})



def listar_contenidos(request):
    """
    Lista todos los contenidos disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de contenidos.
    """

    contenidos = Contenido.objects.all() 
    return render(request, 'listar_contenidos.html', {'contenidos': contenidos})


def contenido_detalle(request, pk):
    """
    Muestra detalles de un contenido específico.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        pk (int): ID del contenido a mostrar detalles.
        
    Returns:
        HttpResponse: Renderiza la página de detalles del contenido.
    """

    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'contenido_detalle.html', {'contenido': contenido})

@login_required



def modificar_categoria(request):

    """
    Permite modificar una categoría existente.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de modificación de categoría o guarda los cambios en la base de datos.
    """

    categorias = Categoria.objects.all()  # Obtén todas las categorías
    categoria = None

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'seleccionar':
            categoria_id = request.POST.get('categoria')
            categoria = get_object_or_404(Categoria, pk=categoria_id)
        elif accion == 'guardar':
            categoria_id = request.POST.get('categoria_id')
            categoria = get_object_or_404(Categoria, pk=categoria_id)
            categoria.nombre = request.POST.get('nombre')
            categoria.descripcion = request.POST.get('descripcion')
            categoria.save()
            # Redirige a donde desees después de guardar los cambios

    return render(request, 'modificar_categoria.html', {'categorias': categorias, 'categoria': categoria})



def crear_subcategoria(request):

    """
    Crea una nueva subcategoría y la guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de subcategoría o redirige tras la creación exitosa.
    """

    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            categoria_id = request.POST.get('categoria_relacionada')
            subcategoria_existente_id = request.POST.get('subcategoria_existente')
            nombre = form.cleaned_data.get('nombre')

            # Verificar si la subcategoría ya existe en cualquier categoría
            if Subcategoria.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, 'Esta subcategoría ya existe. Por favor, cree una nueva.')
            else:
                if categoria_id and subcategoria_existente_id:
                    # Asociar subcategoría existente con la categoría seleccionada
                    categoria = Categoria.objects.get(pk=categoria_id)
                    subcategoria_existente = Subcategoria.objects.get(pk=subcategoria_existente_id)
                    subcategoria_existente.categoria_relacionada = categoria
                    subcategoria_existente.save()
                else:
                    # Crear una nueva subcategoría
                    subcategoria = form.save(commit=False)
                    subcategoria.categoria_relacionada = Categoria.objects.get(pk=categoria_id)
                    subcategoria.save()
                    return redirect('ver_subcategoria', subcategoria_id=subcategoria.id)
        
        else:
            messages.error(request, 'Por favor, completa todos los campos correctamente.')

    else:
        form = SubcategoriaForm()

    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    return render(request, 'crear_subcategoria.html', {'form': form, 'categorias': categorias, 'subcategorias': subcategorias})



def listar_subcategorias(request):

    """
    Lista todas las subcategorías disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de subcategorías.
    """

    # Aquí coloca la lógica para obtener y listar las subcategorías desde la base de datos
    subcategorias = Subcategoria.objects.all()
    return render(request, 'listar_subcategorias.html', {'subcategorias': subcategorias})



def ver_subcategoria(request, subcategoria_id):

    """
    Muestra detalles de una subcategoría específica.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        subcategoria_id (int): ID de la subcategoría a mostrar detalles.
        
    Returns:
        HttpResponse: Renderiza la página de detalles de la subcategoría.
    """
        
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
    return render(request, 'ver_subcategoria.html', {'subcategoria': subcategoria})



def modificar_subcategoria(request, subcategoria_id):

    """
    Permite modificar una subcategoría existente.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        subcategoria_id (int): ID de la subcategoría a modificar.
        
    Returns:
        HttpResponse: Renderiza la página de modificación de subcategoría o guarda los cambios en la base de datos.
    """
        
    subcategoria = Subcategoria.objects.get(pk=subcategoria_id)

    if request.method == 'POST':
        # Procesar el formulario de modificación y guardar los cambios en la base de datos
        subcategoria.nombre = request.POST['nombre']
        subcategoria.descripcion = request.POST['descripcion']
        subcategoria.save()
        return redirect(reverse('listar_subcategorias'))  # Puedes redirigir a donde desees

    return render(request, 'modificar_subcategoria.html', {'subcategoria': subcategoria})




#Definicio de vista para los roles
def vista_autor(request):

    """
    Muestra una vista para usuarios con el rol de "Autor".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de vista para lectores o muestra un mensaje de error si el usuario no tiene el rol adecuado.
    """
        
    # Asegurarse de que el usuario tiene el rol de autor
    if not request.user.usuario.rol.nombre == 'Autor':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    # Obtener todos los posts
    posts = Contenido.objects.all()  # Asumiendo que tienes un modelo llamado Contenido para los posts

    return render(request, 'vista_autor.html', {'posts': posts})

def vista_editores(request):

    """
    Muestra una vista para usuarios con el rol de "Editores".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de vista para Editores o muestra un mensaje de error si el usuario no tiene el rol adecuado.
    """
        
    # Asegurarse de que el usuario tiene el rol de Editor
    if not request.user.usuario.rol.nombre == 'Editores':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    # Obtener todos los posts
    posts = Contenido.objects.all()  # Asumiendo que tienes un modelo llamado Contenido para los posts

    return render(request, 'vista_editores.html', {'posts': posts})

def vista_publicador(request):

    """
    Muestra una vista para usuarios con el rol de "Publicador".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de vista para Publicadores o muestra un mensaje de error si el usuario no tiene el rol adecuado.
    """
        
    # Asegurarse de que el usuario tiene el rol de Publicador
    if not request.user.usuario.rol.nombre == 'Publicadores':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    # Obtener todos los posts
    posts = Contenido.objects.all()  # Asumiendo que tienes un modelo llamado Contenido para los posts

    return render(request, 'vista_publicador.html', {'posts': posts})

def vista_suscriptor(request):

    """
    Muestra una vista para usuarios con el rol de "Suscriptor".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de vista para Suscriptor o muestra un mensaje de error si el usuario no tiene el rol adecuado.
    """
        
    # Asegurarse de que el usuario tiene el rol de Publicador
    if not request.user.usuario.rol.nombre == 'Suscriptor':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    # Obtener todos los posts
    posts = Contenido.objects.all()  # Asumiendo que tienes un modelo llamado Contenido para los posts

    return render(request, 'vista_suscriptor.html', {'posts': posts})

def toggle_active_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'success': True})

def toggle_user_active(request, user_id):
    # Aquí va tu lógica para activar/desactivar el usuario
    # Por ejemplo, cambiar el campo is_active en el modelo User
    # Luego, devolver una respuesta basada en el resultado

    user = User.objects.get(pk=user_id)
    user.is_active = not user.is_active
    user.save()

    return JsonResponse({'success': True, 'is_active': user.is_active})

def eliminar_rol(request, rol_id):
    """
    Vista que permite eliminar un rol.

    Parámetros:
        request: Objeto de solicitud HTTP.
        rol_id: Identificador del rol a eliminar.

    Retorna:
        HttpResponse: Redirige a la vista 'listar_roles' después de la eliminación.
                      Muestra la confirmación de eliminación antes de la acción.

    Comportamiento:
        - Obtiene el objeto Rol con el identificador proporcionado.
        - Si la solicitud es de tipo POST, elimina el rol y redirige a la vista 'listar_roles'.
        - Si la solicitud no es de tipo POST, muestra la página de confirmación de eliminación.
    """
    rol = get_object_or_404(Rol, pk=rol_id)
    if request.method == "POST":  # Si el método es POST, significa que el usuario ha confirmado la eliminación
        rol.delete()
        return redirect('listar_roles')
    return render(request, 'confirmar_eliminacion.html', {'rol': rol})

def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre')
    if Rol.objects.filter(nombre=nombre).exists():
        raise forms.ValidationError("Este rol ya existe.")
    return nombre

def modificar_rol(request, rol_id):
    rol_instance = get_object_or_404(Rol, pk=rol_id)
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol modificado con éxito.')
            return redirect('listar_roles')
    else:
        form = RolForm(instance=rol_instance)

    return render(request, 'modificar_rol.html', {'form': form, 'rol': rol_instance})



def crear_tipo_de_contenido(request):

    """
    Vista que permite la creación de un nuevo tipo de contenido.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponseRedirect o HttpResponse: 
            - Si la solicitud es un POST y los datos del formulario son válidos, se crea un nuevo tipo de contenido y se redirige a la página deseada.
            - Si la solicitud es un POST pero los datos del formulario no son válidos o el tipo de contenido ya existe, se muestra un mensaje de error y se vuelve a mostrar el formulario.
            - Si la solicitud es un GET, se muestra el formulario vacío para la creación de un nuevo tipo de contenido.
    """
    
    if request.method == 'POST':
        form = TipoDeContenidoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            plantilla = form.cleaned_data['plantilla'] 

            # Verificar si el tipo de contenido ya existe
            if TipoDeContenido.objects.filter(nombre__iexact=nombre).exists():
                messages.error(request, 'Este tipo de contenido ya existe. Por favor crea uno nuevo')
            else:
                form.save()
                
                return redirect('profile_view')  # Puedes redirigir a la página deseada
            
        else:
            messages.error(request, 'Por favor, completa todos los campos correctamente.')
    else:
        form = TipoDeContenidoForm()
    return render(request, 'crear_tipo_de_contenido.html', {'form': form})



def listar_tipos_de_contenido(request):

    """
    Vista que muestra una lista de tipos de contenido.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: 
            - Muestra una página que lista todos los tipos de contenido disponibles, junto con sus nombres de plantilla si están asociados.
    """

    tipos_de_contenido = TipoDeContenido.objects.all()

    for tipo in tipos_de_contenido:
        tipo.plantilla_nombre = tipo.plantilla.nombre if tipo.plantilla else "N/A"

    return render(request, 'listar_tipos_de_contenido.html', {'tipos_de_contenido': tipos_de_contenido})


def crear_contenido(request):
    if request.method == "POST":
        tipo_de_contenido_id = request.POST.get('tipo_de_contenido')
        tipo_de_contenido = get_object_or_404(TipoDeContenido, pk=tipo_de_contenido_id)
        
        form = CrearContenidoForm(request.POST, request.FILES)  # Añade request.FILES aquí
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.autor = request.user
            contenido.tipo = tipo_de_contenido
            contenido.plantilla = tipo_de_contenido.plantilla
            # Si tu modelo 'Contenido' tiene un campo para imagen, se guardará aquí
            contenido.save()
            form.save_m2m()  # Si tu modelo tiene relaciones ManyToMany que necesiten guardarse
            return redirect('listar_contenidos')
    else:
        tipos = TipoDeContenido.objects.all()
        form = CrearContenidoForm()

    return render(request, 'crear_contenido.html', {'form': form, 'tipos': tipos})


def vista_de_formulario(request):
    """
    Vista que muestra el formulario de creación de contenido.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la página de creación de contenido con el formulario y las plantillas disponibles.
    """
    
    plantillas = Plantilla.objects.all()
    form = CrearContenidoForm()
    return render(request, 'crear_contenido.html', {'form': form, 'plantillas': plantillas})



def get_plantilla_por_tipo(request, tipo_id):
    try:
        tipo = TipoDeContenido.objects.get(pk=tipo_id)
        if tipo.plantilla:
            nombre_plantilla = tipo.plantilla.tipo
            soporte_multimedia = 'multimedia' in nombre_plantilla.lower()  # Verifica si es multimedia
        else:
            nombre_plantilla = 'No hay plantilla asociada'
            soporte_multimedia = False

        return JsonResponse({'plantilla': nombre_plantilla, 'soporte_multimedia': soporte_multimedia})
    except TipoDeContenido.DoesNotExist:
        return JsonResponse({'error': 'Tipo de contenido no encontrado'}, status=404)


def revisar_contenido(request, contenido_id):
    """
    Cambia el estado de un contenido a 'En Revisión'.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a revisar.

    Returns:
        HttpResponse: Renderiza la página de detalles del contenido revisado.
    """

    contenido = get_object_or_404(Contenido, pk=contenido_id)
    contenido.estado = Contenido.ESTADO_EN_REVISION
    contenido.save()
    # Puedes agregar lógica adicional según tus necesidades
    return render(request, 'detalle_contenido.html', {'contenido': contenido})


def aprobar_contenido(request, contenido_id):
    """
    Cambia el estado de un contenido a 'Publicado'.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a aprobar.

    Returns:
        HttpResponse: Renderiza la página de detalles del contenido aprobado.
    """

    contenido = get_object_or_404(Contenido, pk=contenido_id)
    contenido.estado = Contenido.ESTADO_PUBLICADO
    contenido.save()
    
    # Generar notificación de aprobación
    usuario_contenido = contenido.autor
    mensaje = f"Tu contenido '{contenido.titulo}' ha sido aprobado y ahora está publicado."
    Notificacion.objects.create(usuario=usuario_contenido, mensaje=mensaje)

    return render(request, 'detalle_contenido.html', {'contenido': contenido})

# En views.py
def desaprobar_contenido(request, contenido_id):
    """
    Cambia el estado de un contenido a 'Rechazado' con un comentario opcional.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a desaprobar.

    Returns:
        HttpResponse: Renderiza la página de detalles del contenido desaprobado o muestra el formulario de desaprobación.
    """

    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, pk=contenido_id)
        contenido.estado = Contenido.ESTADO_RECHAZADO
        contenido.comentario = request.POST.get('comentario', '')
        contenido.save()
        # Puedes agregar lógica adicional según tus necesidades

        # Generar notificación de rechazo
        usuario_contenido = contenido.autor
        mensaje = f"Tu contenido '{contenido.titulo}' ha sido rechazado. Comentario del revisor: {contenido.comentario}"
        Notificacion.objects.create(usuario=usuario_contenido, mensaje=mensaje)

        # Notificar al usuario usando la función notificar_usuario
        notificar_usuario(usuario_contenido.id, mensaje)

        return render(request, 'detalle_contenido.html', {'contenido': contenido})
    else:
        contenido = get_object_or_404(Contenido, pk=contenido_id)
        return render(request, 'desaprobar_contenido.html', {'contenido': contenido})


def inactivar_contenido(request, contenido_id):
    """
    Cambia el estado de un contenido a 'Inactivo'.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a inactivar.

    Returns:
        HttpResponse: Renderiza la página de detalles del contenido inactivado.
    """

    contenido = get_object_or_404(Contenido, pk=contenido_id)
    contenido.estado = Contenido.ESTADO_INACTIVO
    contenido.save()

    # Puedes agregar lógica adicional según tus necesidades
    return render(request, 'detalle_contenido.html', {'contenido': contenido})


# proyecto_CMS/Seguridad/views.py

def cancelar_agregar_contenido(request, contenido_id):
    """
    Cancela la operación de agregar contenido y elimina el contenido.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a cancelar y eliminar.

    Returns:
        HttpResponseRedirect: Redirige a la vista de perfil o a donde consideres necesario.
    """

    contenido = get_object_or_404(Contenido, pk=contenido_id)
    
    # Asegúrate de agregar lógica adicional si es necesario antes de eliminar el contenido
    contenido.delete()
    
    # Puedes redirigir a donde sea apropiado en tu aplicación
    return redirect('profile_view')  # Redirige a la vista de perfil o a donde consideres necesario



def detalle_contenido(request, contenido_id):
    """
    Muestra detalles de un contenido específico.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        contenido_id (int): ID del contenido a mostrar detalles.

    Returns:
        HttpResponse: Renderiza la página de detalles del contenido.
    """

    contenido = get_object_or_404(Contenido, pk=contenido_id)

    # Obtén las notificaciones asociadas al usuario autor del contenido
    notificaciones = Notificacion.objects.filter(usuario=contenido.autor.user)

    # Marca las notificaciones como leídas
    notificaciones.update(leida=True)

    return render(request, 'detalle_contenido.html', {'contenido': contenido, 'notificaciones': notificaciones})
# proyecto_CMS/Seguridad/views.py

# En views.py
def tablero_kanban(request):
    """
    Vista que muestra un tablero Kanban con los contenidos organizados por estado.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la página del tablero Kanban.
    """

    estados = [estado[0] for estado in Contenido.ESTADOS_CHOICES]
    contenidos_por_estado = {estado: Contenido.objects.filter(estado=estado).order_by('posicion') for estado in estados}

    return render(request, 'tablero_kanban.html', {'contenidos_por_estado': contenidos_por_estado})




def cambiar_estado_contenido(request):
    """
    Cambia el estado de un contenido según la solicitud.

    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o fallo de la operación.
    """
        
    if request.method == 'POST':
        contenido_id = request.POST.get('contenido_id')
        nuevo_estado = request.POST.get('nuevo_estado')

        #print(f"Contenido ID: {contenido_id}, Nuevo Estado: {nuevo_estado}")

        try:
            contenido = Contenido.objects.get(id=contenido_id)
            contenido.cambiar_estado(nuevo_estado)

            return JsonResponse({'success': True, 'nuevo_estado': nuevo_estado})
        except Contenido.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Contenido no encontrado'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Valor no válido'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def agregar_like(request, contenido_id):
    """
    Agrega un "like" al contenido especificado.

    Parameters:
    - request: La solicitud HTTP recibida.
    - contenido_id: El ID del contenido al cual se desea agregar el "like".

    Returns:
    - JsonResponse: Respuesta en formato JSON indicando el éxito o fallo de la operación.
    """
    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, pk=contenido_id)
        usuario = request.user.usuario

        # Verificar si el usuario ya dio like
        if not Like.objects.filter(usuario=usuario, contenido=contenido).exists():
            Like.objects.create(usuario=usuario, contenido=contenido)

            # Crear notificación después de dar like
            Notificacion.objects.create(
                usuario=contenido.autor.user,
                mensaje=f"{request.user.username} ha dado like a tu contenido: '{contenido.titulo}'.",
            )

            return JsonResponse({'success': True})
        else:
            # Si el usuario ya dio like, podrías manejarlo de alguna manera (opcional)
            return JsonResponse({'success': False, 'error': 'Ya diste like a este contenido'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def agregar_comentario(request, contenido_id):
    """
    Agrega un comentario al contenido especificado.

    Parameters:
    - request: La solicitud HTTP recibida.
    - contenido_id: El ID del contenido al cual se desea agregar el comentario.

    Returns:
    - JsonResponse: Respuesta en formato JSON indicando el éxito o fallo de la operación.
    """
    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, pk=contenido_id)
        usuario = request.user.usuario
        texto = request.POST.get('texto', '')

        Comentario.objects.create(usuario=usuario, contenido=contenido, texto=texto)

        # Generar notificación de comentario
        usuario_contenido = contenido.autor
        mensaje = f"{request.user.username} ha comentado en tu contenido '{contenido.titulo}': {request.POST.get('comentario')}"
        Notificacion.objects.create(usuario=usuario_contenido, mensaje=mensaje)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def agregar_respuesta(request, comentario_id):
    """
    Agrega una respuesta a un comentario especificado.

    Parameters:
    - request: La solicitud HTTP recibida.
    - comentario_id: El ID del comentario al cual se desea agregar la respuesta.

    Returns:
    - JsonResponse: Respuesta en formato JSON indicando el éxito o fallo de la operación.
    """    
    if request.method == 'POST':
        comentario_padre = get_object_or_404(Comentario, pk=comentario_id)
        usuario = request.user.usuario
        texto = request.POST.get('texto', '')

        RespuestaComentario.objects.create(comentario_padre=comentario_padre, usuario=usuario, texto=texto)

        # Crear notificación después de agregar respuesta
        Notificacion.objects.create(
            usuario=comentario_padre.usuario.user,
            mensaje=f"{request.user.username} ha respondido a tu comentario en el contenido: '{comentario_padre.contenido.titulo}'.",
        )


        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def compartir_contenido(request, contenido_id):
    """
    Comparte un contenido especificado.

    Parameters:
    - request: La solicitud HTTP recibida.
    - contenido_id: El ID del contenido que se desea compartir.

    Returns:
    - JsonResponse: Respuesta en formato JSON indicando el éxito o fallo de la operación.
    """
    if request.method == 'POST':
        contenido = get_object_or_404(Contenido, pk=contenido_id)
        usuario = request.user.usuario

        # Verificar si el usuario ya compartió este contenido
        if not Compartido.objects.filter(usuario=usuario, contenido=contenido).exists():
            Compartido.objects.create(usuario=usuario, contenido=contenido)

            # Crear notificación después de compartir contenido
            Notificacion.objects.create(
                usuario=contenido.autor.user,
                mensaje=f"{request.user.username} ha compartido tu contenido: '{contenido.titulo}'.",
            )

            return JsonResponse({'success': True})
        else:
            # Si el usuario ya compartió el contenido, podrías manejarlo de alguna manera (opcional)
            return JsonResponse({'success': False, 'error': 'Ya compartiste este contenido'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def notificar_usuario(usuario_id, mensaje):
    """
    Notifica a un usuario específico.

    Parameters:
    - usuario_id: El ID del usuario al cual se desea enviar la notificación.
    - mensaje: El mensaje de la notificación.

    Returns:
    - None
    """
    try:
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                f"usuario_{usuario_id}",
                {
                    'type': 'notificacion_event',
                    'mensaje': mensaje
                }
            )
            print(f"Notificación enviada a usuario_{usuario_id}: {mensaje}")
        else:
            print("Error: El channel_layer no está configurado correctamente.")
    except Exception as e:
        print(f"Error al enviar notificación: {e}")

@login_required
def obtener_notificaciones(request):
    """
    Obtiene las notificaciones del usuario autenticado.

    Returns:
        JsonResponse: Respuesta en formato JSON con las notificaciones.
    """
    user = request.user 
    notificaciones = Notificacion.objects.filter(usuario=user, leida=False).values('mensaje', 'fecha_creacion')

    # Obtén el número total de notificaciones no leídas
    notificaciones_no_leidas = Notificacion.objects.filter(usuario=user, leida=False).count()

    return JsonResponse({'notificaciones': list(notificaciones), 'notificaciones_no_leidas': notificaciones_no_leidas})