from django.test import TestCase
import pytest
from django.urls import reverse, resolve
from Seguridad.models import Categoria, Rol, Permiso, Categoria  # Asegúrate de que la importación sea correcta
from django.shortcuts import redirect


# Create your tests here.

@pytest.mark.django_db
def test_crear_categoria(client):
    url = reverse('crear_categoria')  # Reemplaza 'crear_categoria' con el nombre real de la URL en tu aplicación
    data = {'nombre': 'Categoría de prueba', 'descripcion': 'Descripción de prueba'}
    response = client.post(url, data)
    
    assert response.status_code == 302  # Esperamos un redirect después de una creación exitosa
    assert Categoria.objects.count() == 1  # Esperamos que se haya creado una categoría
    assert Categoria.objects.first().nombre == 'Categoría de prueba'  # Comprobamos que la categoría tenga el nombre correcto

@pytest.mark.django_db
def test_listar_categorias(client):
    Categoria.objects.create(nombre='Categoria 1', descripcion='Descripción 1')
    Categoria.objects.create(nombre='Categoria 2', descripcion='Descripción 2')
    
    url = reverse('listar_categorias')  # Reemplaza 'listar_categorias' con el nombre real de la URL en tu aplicación
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'Categoria 1' in str(response.content)
    assert 'Categoria 2' in str(response.content)

@pytest.mark.django_db
def test_crear_roles(client):
    url = reverse('crear_rol')  
    data = {'nombre': 'Rol de prueba', 'descripcion': 'Descripción de prueba'}
    response = client.post(url, data)
    
    assert response.status_code == 200  # Esperamos un redirect después de una creación exitosa
    assert Rol.objects.count() == 0
    #assert Rol.objects.first().nombre == 'Rol de prueba' 

@pytest.mark.django_db
def test_listar_roles (client):
    Rol.objects.create(nombre='Rol 1', descripcion='Descripción 1')
    Rol.objects.create(nombre='Rol 2', descripcion='Descripción 2')
    
    url = reverse('listar_roles')  
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'Rol 1' in str(response.content)
    assert 'Rol 2' in str(response.content)

@pytest.mark.django_db
def test_crear_permiso(client):
    url = reverse('crear_permiso')  # Reemplaza 'crear_permiso' con el nombre real de la URL en tu aplicación
    data = {'nombre': 'Permiso de prueba', 'descripcion': 'Descripción de prueba'}
    response = client.post(url, data)
    
    assert response.status_code == 302  # Esperamos un redirect después de una creación exitosa
    assert Permiso.objects.count() == 1  # Esperamos que se haya creado un permiso
    assert Permiso.objects.first().nombre == 'Permiso de prueba'  # Comprobamos que el permiso tenga el nombre correcto
    assert response.url == reverse('profile_view')  # Cambia esto al nombre real de la vista a la que se redirige  


@pytest.mark.django_db
def test_listar_permisos(client):
    Permiso.objects.create(nombre='Permiso 1', descripcion='Descripción 1')
    Permiso.objects.create(nombre='Permiso 2', descripcion='Descripción 2')
    
    url = reverse('listar_permisos')  # Reemplaza 'listar_permisos' con el nombre real de la URL en tu aplicación
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'Permiso 1' in str(response.content)
    assert 'Permiso 2' in str(response.content)


