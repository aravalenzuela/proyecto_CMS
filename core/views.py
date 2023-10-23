from django.http import HttpResponse
from django.shortcuts import redirect, render
import hashlib
from Seguridad.models import Usuario, Rol  # Asegúrate de que este modelo exista y tenga un campo 'role'


def get_gravatar_url(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=150"

def home(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def login_with_google(oauth_code):
    # Supongamos que esta función usa oauth_code para obtener un token de Google
    # y luego inicia sesión al usuario en tu aplicación
    pass
def logout(request):
    """
    Redirecciona a la pagina de cerrar sesion de google
    :param request: HttpRequest object
    :return:HttpRedirect
    """
    return redirect('/accounts/logout/')

def profile_view(request):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirige al usuario a la vista de inicio de sesión

    # Obtiene el email del usuario y su avatar
    user_email = request.user.email
    gravatar_url = get_gravatar_url(user_email)

    # Obtiene el perfil del usuario y su rol
    try:
        user_profile = Usuario.objects.get(user=request.user)
        user_role = user_profile.rol.id
    except Usuario.DoesNotExist:
        user_role = None

    # Basado en el rol, decides a qué vista redirigir
    if user_role == 12:
        return redirect('admin_dashboard')
    elif user_role == 4:
        return render(request, 'profile.html')
    elif user_role == 5 :
        return render(request, 'vista_lector.html')

    # Si no tiene un rol específico o es un rol desconocido, muestra su perfil con Gravatar
    return render(request, 'profile.html', {'gravatar_url': gravatar_url})



