# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

#python manage.py runscript load_plantillas.py,,,, comando

# Crear instancias de plantillas
plantilla350 = Plantilla(nombre="Blog", tipo="blog", contenidoDePlantilla="Contenido de la plantilla Blog")
plantilla350.save()
plantilla351 = Plantilla(nombre="Multimedia", tipo="multimedia", contenidoDePlantilla="Contenido de la plantilla Multimedia")
plantilla351.save()



# Agrega más plantillas si es necesario
