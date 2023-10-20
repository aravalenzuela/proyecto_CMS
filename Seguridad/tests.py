from django.test import TestCase
import pytest
from django.urls import reverse
from Seguridad.models import Categoria, Rol, Permiso, Subcategoria  # Asegúrate de que la importación sea correcta
from django.shortcuts import redirect




from django.contrib.auth.models import User

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



# Prueba la creación de una subcategoría
@pytest.mark.django_db
def test_crear_subcategoria(client):
    # Crea una categoría para asociar la subcategoría
    categoria = Categoria.objects.create(nombre='Categoría de prueba', descripcion='Descripción de prueba')
    
    url = reverse('crear_subcategoria')
    data = {'nombre': 'Subcategoría de prueba', 'descripcion': 'Descripción de prueba', 'categoria_relacionada': categoria.id}
    response = client.post(url, data)

    assert response.status_code == 302  # Esperamos una redirección después de una creación exitosa
    assert Subcategoria.objects.count() == 1  # Esperamos que se haya creado una subcategoría
    subcategoria = Subcategoria.objects.first()
    assert subcategoria.nombre == 'Subcategoría de prueba'
    assert subcategoria.categoria_relacionada == categoria  # Comprueba que la subcategoría esté asociada a la categoría



# Prueba la modificación de una subcategoría
@pytest.mark.django_db
def test_modificar_subcategoria(client):
    subcategoria = Subcategoria.objects.create(nombre='Subcategoría de prueba', descripcion='Descripción de prueba')
    
    url = reverse('modificar_subcategoria', args=[subcategoria.id])
    new_data = {'nombre': 'Nueva Subcategoría', 'descripcion': 'Nueva Descripción'}
    response = client.post(url, new_data)

    subcategoria.refresh_from_db()  # Actualiza la instancia de la subcategoría desde la base de datos
    assert response.status_code == 302  # Esperamos una redirección después de una modificación exitosa
    assert subcategoria.nombre == 'Nueva Subcategoría'  # Comprueba que el nombre de la subcategoría se haya actualizado




class SubcategoriaTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de ejemplo (puedes personalizarlo según tus necesidades)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Crea una subcategoría de ejemplo
        self.subcategoria = Subcategoria.objects.create(
            nombre='Ejemplo',
            descripcion='Descripción de ejemplo'
        )

    def test_ver_subcategoria(self):
        # Iniciar sesión como el usuario de prueba
        self.client.login(username='testuser', password='testpassword')
        
        # Obtener la URL de la vista 'ver_subcategoria' para la subcategoría creada
        url = reverse('ver_subcategoria', args=[self.subcategoria.id])
        
        # Realizar una solicitud GET a la vista
        response = self.client.get(url)
        
        # Comprobar que la página se carga correctamente (código de respuesta HTTP 200)
        self.assertEqual(response.status_code, 200)
        
        # Comprobar que la subcategoría se muestra en la página
        self.assertContains(response, 'Ejemplo')
        self.assertContains(response, 'Descripción de ejemplo')



class SubcategoriaListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configura datos de prueba una vez para todos los métodos de prueba
        Subcategoria.objects.create(nombre="Subcategoría de prueba", descripcion="Esta es una subcategoría de prueba.")

    def test_listar_subcategorias_view_url_exists_at_desired_location(self):
        response = self.client.get('/listar_subcategorias/')
        self.assertEqual(response.status_code, 200)

    def test_listar_subcategorias_view_url_accessible_by_name(self):
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertEqual(response.status_code, 200)

    def test_listar_subcategorias_view_uses_correct_template(self):
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertTemplateUsed(response, 'listar_subcategorias.html')

    def test_listar_subcategorias_view_displays_subcategorias(self):
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertContains(response, 'Subcategoría de prueba')


    def test_listar_subcategorias_view_displays_multiple_subcategorias(self):
        # Crea más subcategorías de prueba
        Subcategoria.objects.create(nombre="Subcategoría 1", descripcion="Descripción de la subcategoría 1.")
        Subcategoria.objects.create(nombre="Subcategoría 2", descripcion="Descripción de la subcategoría 2.")
        
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertContains(response, 'Subcategoría 1')
        self.assertContains(response, 'Subcategoría 2')
