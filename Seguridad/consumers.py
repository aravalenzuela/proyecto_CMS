import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionesConsumer(AsyncWebsocketConsumer):
    """
    Consumidor de WebSockets para manejar notificaciones en tiempo real.
    """
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def notificacion_event(self, event):
        mensaje = event['mensaje']

        await self.send(text_data=json.dumps({
            'mensaje': mensaje
        }))