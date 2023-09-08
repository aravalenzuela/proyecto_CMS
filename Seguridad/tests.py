from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from Seguridad.models import Categoria  # Asegúrate de que la importación sea correcta

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
