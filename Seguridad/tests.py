from django.test import TestCase
import pytest
from django.urls import reverse
from Seguridad.models import Categoria, Rol, Permiso, Subcategoria, TipoDeContenido, Contenido # Asegúrate de que la importación sea correcta
from django.shortcuts import redirect
from django.db.utils import IntegrityError

from django.shortcuts import get_object_or_404
from Seguridad.views import listar_tipos_de_contenido, modificar_estado_categoria
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

@pytest.mark.django_db
def test_modificar_estado_categoria_view(client):

    """
    Prueba unitaria para la vista que modifica el estado de una categoría.

    Parameters:
        client (Client): Un cliente de prueba para realizar solicitudes HTTP.

    Returns:
        None

    """

    # Crear una instancia de la categoría
    categoria = Categoria.objects.create(nombre="Categoría de prueba", activo=True)

    # Realizar una solicitud POST a la vista con el ID de la categoría
    response = client.post(reverse('modificar_estado_categoria', args=[categoria.pk]))

    # Verificar que la solicitud fue exitosa (código de respuesta HTTP 302 para la redirección)
    assert response.status_code == 302

    # Verificar que la categoría cambió su estado a inactivo (activo=False)
    categoria_actualizada = Categoria.objects.get(pk=categoria.pk)
    assert not categoria_actualizada.activo

@pytest.mark.django_db
def test_modificar_estado_categoria_view_category_not_found(client):

    """
    Prueba unitaria para la vista que intenta modificar el estado de una categoría que no existe.

    Parameters:
        client (Client): Un cliente de prueba para realizar solicitudes HTTP.

    Returns:
        None

    """

    # Intentar modificar el estado de una categoría que no existe
    response = client.post(reverse('modificar_estado_categoria', args=[999]))  # ID no existente

    # Verificar que la categoría no se encontró y se devuelve una respuesta JSON con un código de estado 404
    assert response.status_code == 404
    assert response.json() == {'mensaje': 'Categoría no encontrada'}


@pytest.mark.django_db
def test_listar_tipos_de_contenido_view(client):

    """
    Prueba unitaria para la vista que lista los tipos de contenido.

    Parameters:
        client (Client): Un cliente de prueba para realizar solicitudes HTTP.

    Returns:
        None

    """
    # Crear instancias de TipoDeContenido (puedes ajustar esto según tus necesidades)
    tipo1 = TipoDeContenido.objects.create(nombre="Tipo 1")
    tipo2 = TipoDeContenido.objects.create(nombre="Tipo 2")

    # Realizar una solicitud GET a la vista
    response = client.get(reverse('listar_tipos_de_contenido'))  # Ajusta el nombre de la URL según tu proyecto

    # Verificar que la solicitud fue exitosa (código de respuesta HTTP 200)
    assert response.status_code == 200

    # Verificar que los objetos TipoDeContenido se muestran en la respuesta
    assert tipo1.nombre.encode() in response.content
    assert tipo2.nombre.encode() in response.content

    # También puedes verificar otros aspectos de la respuesta, como la plantilla utilizada

    # Por ejemplo, verifica que se está utilizando la plantilla 'listar_tipos_de_contenido.html'
    assert 'listar_tipos_de_contenido.html' in [template.name for template in response.templates]

    # También puedes verificar que el contexto de la vista es correcto
    assert 'tipos_de_contenido' in response.context

    # Verificar que el contexto contiene los objetos TipoDeContenido
    assert tipo1 in response.context['tipos_de_contenido']
    assert tipo2 in response.context['tipos_de_contenido']

@pytest.mark.django_db
def test_contenido_creation():

    """
    Prueba unitaria para la creación de una instancia de Contenido.

    Returns:
        None

    """
    # Crear instancias de TipoDeContenido y User para usar en la prueba
    tipo_de_contenido = TipoDeContenido.objects.create(nombre="Ejemplo")
    user = User.objects.create_user(username="usuario", password="contraseña")

    # Crear una instancia de Contenido
    contenido = Contenido(
        tipo=tipo_de_contenido,
        titulo="Título de ejemplo",
        cuerpo="Cuerpo de ejemplo",
        autor=user,
    )
    contenido.save()

    # Comprobar que la instancia se ha guardado correctamente en la base de datos
    assert Contenido.objects.count() == 1

    # Comprobar que los atributos se han guardado correctamente
    contenido_guardado = Contenido.objects.first()
    assert contenido_guardado.tipo == tipo_de_contenido
    assert contenido_guardado.titulo == "Título de ejemplo"
    assert contenido_guardado.cuerpo == "Cuerpo de ejemplo"
    assert contenido_guardado.autor == user

@pytest.mark.django_db
def test_contenido_str_method():
    """
    Prueba unitaria para el método __str__ de la clase Contenido.

    Returns:
        None

    """

    tipo_de_contenido = TipoDeContenido.objects.create(nombre="Ejemplo")
    user = User.objects.create_user(username="usuario", password="contraseña")
    contenido = Contenido(
        tipo=tipo_de_contenido,
        titulo="Título de ejemplo",
        cuerpo="Cuerpo de ejemplo",
        autor=user,
    )

    # Comprobar que el método __str__ devuelve el título del contenido
    assert str(contenido) == "Título de ejemplo"


@pytest.mark.django_db
def test_tipo_de_contenido_creation():
    """
    Prueba unitaria para la creación de una instancia de TipoDeContenido.

    Returns:
        None

    """

    # Crear una instancia de TipoDeContenido
    tipo_de_contenido = TipoDeContenido(
        nombre="Ejemplo",
        descripcion="Descripción de ejemplo",
    )
    tipo_de_contenido.save()

    # Comprobar que la instancia se ha guardado correctamente en la base de datos
    assert TipoDeContenido.objects.count() == 1

    # Comprobar que los atributos se han guardado correctamente
    tipo_guardado = TipoDeContenido.objects.first()
    assert tipo_guardado.nombre == "Ejemplo"
    assert tipo_guardado.descripcion == "Descripción de ejemplo"

@pytest.mark.django_db
def test_tipo_de_contenido_str_method():
    """
    Prueba unitaria para el método __str__ de la clase TipoDeContenido.

    Returns:
        None

    """
    tipo_de_contenido = TipoDeContenido(
        nombre="Ejemplo",
        descripcion="Descripción de ejemplo",
    )

    # Comprobar que el método __str__ devuelve el nombre del tipo de contenido
    assert str(tipo_de_contenido) == "Ejemplo"

