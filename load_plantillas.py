# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla350 = Plantilla(nombre="Plantilla 350", tipo="blog", contenidoDePlantilla="Contenido de la plantilla 350")
plantilla350.save()
plantilla351 = Plantilla(nombre="Plantilla 351", tipo="multimedia", contenidoDePlantilla="Contenido de la plantilla 351")
plantilla351.save()



# Agrega más plantillas si es necesario
