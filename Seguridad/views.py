from django.http import HttpResponse
from django.shortcuts import render
from .models import Permiso
from django.contrib.auth.models import User

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
