## Guía de Ejecución

### Prerrequisitos

- Python 3 instalado en tu sistema.
- Pip (el gestor de paquetes de Python) instalado.

### Instrucciones

1. *Crear un entorno virtual*

   Crea un entorno virtual para instalar las dependencias del proyecto sin afectar las configuraciones globales de tu sistema:

   python3 -m venv venv
   


2. *Activar el entorno virtual*

   Activa el entorno virtual. Este paso es necesario para que las dependencias se instalen y se ejecuten en un entorno aislado.

    . venv/bin/activate

   

3. *Instalar dependencias*

   Instala todas las dependencias necesarias para el proyecto usando el archivo requirements.txt:

   pip install -r requirements.txt

   

4. *Aplicar migraciones*

   Realiza las migraciones necesarias para configurar la base de datos:

   python manage.py makemigrations
   python manage.py migrate

   

5. *Ejecutar el servidor de desarrollo*

   python manage.py runserver

   

6. *Acceder a la aplicación*

   Abre tu navegador y ve a [http://127.0.0.1:8000](http://127.0.0.1:8000).

- Para desactivar el entorno virtual, simplemente ejecuta:

  bash
  deactivate
  

- Asegúrate de mantener el archivo requirements.txt actualizado con cualquier nueva dependencia que agregues al proyecto.
