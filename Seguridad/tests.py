from django.test import TestCase
import pytest
from django.urls import reverse
from Seguridad.models import Categoria, Rol, Permiso, Subcategoria  # Asegúrate de que la importación sea correcta
from django.shortcuts import redirect


from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User


# Prueba la creación de una categoría
@pytest.mark.django_db
def test_crear_categoria(client):

    """
    Prueba la creación de una categoría mediante una solicitud POST.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        La categoría se crea con éxito, y se verifica que se haya creado correctamente.
    """
        
    # Prueba que se puede crear una categoría
    url = reverse('crear_categoria')  # URL para crear una categoría
    data = {'nombre': 'Categoría de prueba', 'descripcion': 'Descripción de prueba'}    # Datos para la creación
    response = client.post(url, data)   # Realiza la solicitud POST
    
    assert response.status_code == 302  # Esperamos una redirección después de la creación exitosa
    assert Categoria.objects.count() == 1   # Comprueba que se haya creado una categoría
    assert Categoria.objects.first().nombre == 'Categoría de prueba'  # Comprobamos que la categoría tenga el nombre correcto




# Prueba la lista de categorías
@pytest.mark.django_db
def test_listar_categorias(client):

    """
    Prueba la visualización de una lista de categorías.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        Se verifican la carga de la página, la presencia de las categorías en la respuesta y su correcta visualización.
    """
        
    # Crea dos categorías de prueba
    Categoria.objects.create(nombre='Categoria 1', descripcion='Descripción 1')
    Categoria.objects.create(nombre='Categoria 2', descripcion='Descripción 2')
    
    url = reverse('listar_categorias')  # URL para listar categorías
    response = client.get(url)   # Realiza la solicitud GET
     
    assert response.status_code == 200     # Comprueba que la página se carga correctamente
    assert 'Categoria 1' in str(response.content)   # Verifica la presencia de la primera categoría en la respuesta
    assert 'Categoria 2' in str(response.content)   # Verifica la presencia de la segunda categoría en la respuesta




# Prueba la creación de un rol
@pytest.mark.django_db
def test_crear_roles(client):

    """
    Prueba la creación de un rol mediante una solicitud POST.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        La creación del rol no debe ser exitosa, y no se debe crear ningún rol.
    """
        
    url = reverse('crear_rol')    # URL para crear un rol
    data = {'nombre': 'Rol de prueba', 'descripcion': 'Descripción de prueba'}    # Datos para la creación
    response = client.post(url, data)     # Realiza la solicitud POST
    
    assert response.status_code == 200  # Esperamos un error ya que no se espera la creación de un rol
    assert Rol.objects.count() == 0     # Comprueba que no se haya creado ningún rol
    #assert Rol.objects.first().nombre == 'Rol de prueba' 




# Prueba la lista de roles
@pytest.mark.django_db
def test_listar_roles (client):

    """
    Prueba la visualización de una lista de roles.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        Se verifican la carga de la página, la presencia de los roles en la respuesta y su correcta visualización.
    """
        
    # Crea dos roles de prueba
    Rol.objects.create(nombre='Rol 1', descripcion='Descripción 1')
    Rol.objects.create(nombre='Rol 2', descripcion='Descripción 2')
    
    url = reverse('listar_roles')   # URL para listar roles
    response = client.get(url)      # Realiza la solicitud GET
    
    assert response.status_code == 200       # Comprueba que la página se carga correctamente
    assert 'Rol 1' in str(response.content)  # Verifica la presencia del primer rol en la respuesta
    assert 'Rol 2' in str(response.content)  # Verifica la presencia del segundo rol en la respuesta 



# Prueba la creación de un permiso
@pytest.mark.django_db
def test_crear_permiso(client):

    """
    Prueba la creación de un permiso mediante una solicitud POST.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        Se crea el permiso con éxito y se verifica que se haya creado correctamente. Luego, se redirige a la vista de perfil.
    """
        
    url = reverse('crear_permiso')   # URL para crear un permiso
    data = {'nombre': 'Permiso de prueba', 'descripcion': 'Descripción de prueba'}  # Datos para la creación
    response = client.post(url, data)    # Realiza la solicitud POST
    
    assert response.status_code == 302  # Esperamos una redirección después de la creación exitosa
    assert Permiso.objects.count() == 1  # Comprueba que se haya creado un permiso
    assert Permiso.objects.first().nombre == 'Permiso de prueba'  # Comprobamos que el permiso tenga el nombre correcto
    assert response.url == reverse('profile_view')  # Comprueba la redirección a la vista de perfil




# Prueba la lista de permisos
@pytest.mark.django_db
def test_listar_permisos(client):

    """
    Prueba la visualización de una lista de permisos.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        Se verifican la carga de la página, la presencia de los permisos en la respuesta y su correcta visualización.
    """
        
    # Crea dos permisos de prueba
    Permiso.objects.create(nombre='Permiso 1', descripcion='Descripción 1')
    Permiso.objects.create(nombre='Permiso 2', descripcion='Descripción 2')
    
    url = reverse('listar_permisos')  # URL para listar permisos
    response = client.get(url)      # Realiza la solicitud GET
    
    assert response.status_code == 200    # Comprueba que la página se carga correctamente
    assert 'Permiso 1' in str(response.content)   # Verifica la presencia del primer permiso en la respuesta
    assert 'Permiso 2' in str(response.content)   # Verifica la presencia del segundo permiso en la respuesta



# Prueba la creación de una subcategoría
@pytest.mark.django_db
def test_crear_subcategoria(client):

    """
    Prueba la creación de una subcategoría mediante una solicitud POST.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        La subcategoría se crea con éxito y se verifica que se haya creado correctamente. Además, se comprueba que esté asociada a una categoría.
    """
        
    # Crea una categoría para asociar la subcategoría
    categoria = Categoria.objects.create(nombre='Categoría de prueba', descripcion='Descripción de prueba')
    
    url = reverse('crear_subcategoria')   # URL para crear una subcategoría
    data = {'nombre': 'Subcategoría de prueba', 'descripcion': 'Descripción de prueba', 'categoria_relacionada': categoria.id}
    response = client.post(url, data)   # Realiza la solicitud POST

    assert response.status_code == 302  # Esperamos una redirección después de una creación exitosa
    assert Subcategoria.objects.count() == 1  # Esperamos que se haya creado una subcategoría
    subcategoria = Subcategoria.objects.first()
    assert subcategoria.nombre == 'Subcategoría de prueba'
    assert subcategoria.categoria_relacionada == categoria  # Comprueba que la subcategoría esté asociada a la categoría




# Prueba la modificación de una subcategoría
@pytest.mark.django_db
def test_modificar_subcategoria(client):

    """
    Prueba la modificación de una subcategoría mediante una solicitud POST.

    Args:
        client (Client): Cliente de prueba de Django.

    Resultados:
        La subcategoría se modifica con éxito y se verifica que los cambios se hayan aplicado correctamente.
    """
        
    subcategoria = Subcategoria.objects.create(nombre='Subcategoría de prueba', descripcion='Descripción de prueba')
    
    url = reverse('modificar_subcategoria', args=[subcategoria.id])
    new_data = {'nombre': 'Nueva Subcategoría', 'descripcion': 'Nueva Descripción'}
    response = client.post(url, new_data)

    subcategoria.refresh_from_db()  # Actualiza la instancia de la subcategoría desde la base de datos
    assert response.status_code == 302  # Esperamos una redirección después de una modificación exitosa
    assert subcategoria.nombre == 'Nueva Subcategoría'  # Comprueba que el nombre de la subcategoría se haya actualizado




# Pruebas para la vista de ver subcategoría
class SubcategoriaTestCase(TestCase):
    def setUp(self):
        """
        Configura los datos de prueba para la vista de ver subcategoría.
        """
                
        # Crea un usuario de ejemplo 
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

        """
        Prueba la visualización de la página de detalle de una subcategoría.

        Resultados:
        La página se carga correctamente, y se verifica que los detalles de la subcategoría se muestran en la página.
        """
                
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




# Pruebas para la vista de listar subcategorías
class SubcategoriaListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Configura los datos de prueba para la vista de listar subcategorías.
        """

        # Configura datos de prueba una vez para todos los métodos de prueba
        Subcategoria.objects.create(nombre="Subcategoría de prueba", descripcion="Esta es una subcategoría de prueba.")

    def test_listar_subcategorias_view_url_exists_at_desired_location(self):

        """
        Prueba si la URL para listar subcategorías existe en la ubicación deseada.

        Resultados:
        Se verifica que la URL existe y responde con un código de estado HTTP 200.
        """
                
        response = self.client.get('/listar_subcategorias/')
        self.assertEqual(response.status_code, 200)


    def test_listar_subcategorias_view_url_accessible_by_name(self):
        """
        Prueba si la URL para listar subcategorías es accesible por su nombre.

        Resultados:
        Se verifica que la URL es accesible por su nombre y responde con un código de estado HTTP 200.
        """
                
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertEqual(response.status_code, 200)


    def test_listar_subcategorias_view_uses_correct_template(self):
        """
        Prueba si la vista de listar subcategorías utiliza la plantilla correcta.

        Resultados:
        Se verifica que la vista utiliza la plantilla 'listar_subcategorias.html'.
        """
                
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertTemplateUsed(response, 'listar_subcategorias.html')


    def test_listar_subcategorias_view_displays_subcategorias(self):
        """
        Prueba si la vista de listar subcategorías muestra subcategorías.

        Resultados:
        Se verifica que la vista carga correctamente, y se comprueba que la página muestra subcategorías en la respuesta.
        """
                
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertContains(response, 'Subcategoría de prueba')


    def test_listar_subcategorias_view_displays_multiple_subcategorias(self):

        """
        Prueba si la vista de listar subcategorías muestra varias subcategorías.

        Resultados:
        Se verifica que la vista carga correctamente, y se comprueba que la página muestra varias subcategorías en la respuesta.
        """
                
        # Crea más subcategorías de prueba
        Subcategoria.objects.create(nombre="Subcategoría 1", descripcion="Descripción de la subcategoría 1.")
        Subcategoria.objects.create(nombre="Subcategoría 2", descripcion="Descripción de la subcategoría 2.")
        
        response = self.client.get(reverse('listar_subcategorias'))
        self.assertContains(response, 'Subcategoría 1')
        self.assertContains(response, 'Subcategoría 2')




# Pruebas para la vista de modificar categoría
class ModificarCategoriaViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Configura los datos de prueba para la vista de modificar categoría.
        """
               
        # Configura datos de prueba una vez para todos los métodos de prueba
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Crea una categoría de prueba
        cls.categoria = Categoria.objects.create(
            nombre='Categoría de prueba',
            descripcion='Descripción de prueba'
        )

    def test_modificar_categoria_view_url_exists_at_desired_location(self):
        """
        Prueba si la URL para modificar categoría existe en la ubicación deseada.

        Resultados:
        Se verifica que la URL existe y responde con un código de estado HTTP 200.
        """
                
        self.client.login(username='testuser', password='testpassword')

        # Cambiar la URL a la que se realiza la solicitud
        url = reverse('modificar_categoria')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



    def test_modificar_categoria_view_url_accessible_by_name(self):
        
        """
        Prueba si la URL para modificar categoría es accesible por su nombre.

        Resultados:
        Se verifica que la URL es accesible por su nombre y responde con un código de estado HTTP 200.
        """
                
        self.client.login(username='testuser', password='testpassword')
        url = reverse('modificar_categoria')

        # Realiza una solicitud GET en lugar de POST para verificar si la página es accesible
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_modificar_categoria_view_select_category(self):

        """
        Prueba la selección de una categoría en la vista de modificar categoría.

        Resultados:
        Se verifica que la página se carga correctamente después de la selección, y se comprueba que los detalles de la categoría seleccionada se muestran en la página.
        """
                
        self.client.login(username='testuser', password='testpassword')

        # Obtén la URL de la vista 'modificar_categoria'
        url = reverse('modificar_categoria')

        # Realiza una solicitud POST para seleccionar una categoría
        response = self.client.post(url, {'accion': 'seleccionar', 'categoria': self.categoria.id})

        # Comprueba que la página se carga correctamente después de la selección
        self.assertEqual(response.status_code, 200)

        # Comprueba que los detalles de la categoría seleccionada se muestran
        self.assertContains(response, 'Nombre: Categoría de prueba')
        self.assertContains(response, 'Descripción: Descripción de prueba')


    def test_modificar_categoria_view_update_category(self):

        """
        Prueba la actualización de una categoría en la vista de modificar categoría.

        Resultados:
        Se verifica que la página se carga correctamente después de la actualización, y se comprueba que los detalles de la categoría actualizada se muestran en la página.
        """
                
        self.client.login(username='testuser', password='testpassword')

        # Obtén la URL de la vista 'modificar_categoria'
        url = reverse('modificar_categoria')

        # Realiza una solicitud POST para seleccionar una categoría
        self.client.post(url, {'accion': 'seleccionar', 'categoria': self.categoria.id})

        # Actualiza la categoría seleccionada
        updated_name = 'Nueva Categoría'
        updated_description = 'Nueva Descripción'
        response = self.client.post(url, {
            'accion': 'guardar',
            'categoria_id': self.categoria.id,
            'nombre': updated_name,
            'descripcion': updated_description
        })

        # Comprueba que la página se carga correctamente después de la actualización
        self.assertEqual(response.status_code, 200)

        # Comprueba que los detalles de la categoría actualizada se muestran
        self.assertContains(response, f'Nombre: {updated_name}')
        self.assertContains(response, f'Descripción: {updated_description}')
