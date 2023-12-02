from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from Seguridad.consumers import NotificacionesConsumer

application = ProtocolTypeRouter({
    
    """
    Configuración del enrutador para manejar los protocolos.
    """
    
    'websocket': URLRouter([
        path('ws/notificaciones/', NotificacionesConsumer.as_asgi()),
    ]),
})