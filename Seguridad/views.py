from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Permiso, Usuario , Categoria, Rol , Contenido, TipoDeContenido, Subcategoria
from django.contrib import messages
from .forms import AsignarPermisoForm
from .forms import CategoriaForm
from .models import Categoria  # Importación relativa
from .forms import CategoriaForm, RolForm
from .models import Categoria, Rol # Importación relativa
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()  # Los permisos se guardarán automáticamente debido a ManyToMany
            messages.success(request, 'Permisos asignados con éxito.')
            return redirect('profile_view')
        else:
            print(form.errors)  # Agregar esta línea para imprimir los errores
            messages.error(request, 'Ha ocurrido un error al asignar los permisos.')
    else:
        form = RolForm(instance=rol)
    
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
            
            # Verificar si la categoría ya existe
            if Categoria.objects.filter(nombre=nombre).exists():
                messages.error(request, 'Esta categoría ya existe. Por favor cree una nueva')
            else:
                form.save()
                return redirect('profile_view')
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
    return render(request, 'lista_contenidos.html', {'contenidos': contenidos})



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
            if Subcategoria.objects.filter(nombre=nombre).exists():
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



def vista_lector(request):

    """
    Muestra una vista para usuarios con el rol de "lector".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de vista para lectores o muestra un mensaje de error si el usuario no tiene el rol adecuado.
    """
        
    # Asegurarse de que el usuario tiene el rol de lector
    if not request.user.usuario.rol.nombre == 'lector':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página")

    # Obtener todos los posts
    posts = Contenido.objects.all()  # Asumiendo que tienes un modelo llamado Contenido para los posts

    return render(request, 'vista_lector.html', {'posts': posts})




def crear_tipo_de_contenido(request):
    if request.method == 'POST':
        form = TipoDeContenidoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            
            # Verificar si el tipo de contenido ya existe
            if TipoDeContenido.objects.filter(nombre=nombre).exists():
                messages.error(request, 'Este tipo de contenido ya existe. Por favor crea uno nuevo')
            else:
                form.save()
                return redirect('profile_view')  # Puedes redirigir a la página deseada
    else:
        form = TipoDeContenidoForm()
    return render(request, 'crear_tipo_de_contenido.html', {'form': form})



def listar_tipos_de_contenido(request):
    tipos_de_contenido = TipoDeContenido.objects.all()
    return render(request, 'listar_tipos_de_contenido.html', {'tipos_de_contenido': tipos_de_contenido})
