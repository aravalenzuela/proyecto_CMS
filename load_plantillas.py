# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla49 = Plantilla(nombre="Plantilla 49", tipo="blog", contenidoDePlantilla="Contenido de la plantilla 49")
plantilla49.save()
plantilla50 = Plantilla(nombre="Plantilla 50", tipo="multimedia", contenidoDePlantilla="Contenido de la plantilla 50")
plantilla50.save()



# Agrega más plantillas si es necesario
