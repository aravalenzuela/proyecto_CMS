from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the Seguridad index.")

def home_view(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

def login_with_google(oauth_code):
    # Supongamos que esta función usa oauth_code para obtener un token de Google
    # y luego inicia sesión al usuario en tu aplicación
    pass

