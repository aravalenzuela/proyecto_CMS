from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Permiso
from django.contrib.auth.models import User
from django.contrib import messages

#Codigos para la implementacion de los requerimientos
def crear_permiso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        permiso = Permiso(nombre=nombre, descripcion=descripcion)
        permiso.save()
        return render(request, 'crear_permiso.html')
    return render(request, 'crear_permiso.html')

def listar_permisos(request):
    permisos = Permiso.objects.all()
    return render(request, 'listar_permisos.html', {'permisos': permisos})

def list_users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def crear_usuario(request):
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

