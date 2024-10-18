import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from whats import Whats
from django.conf import settings
import requests


class MainConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        # Adiciona o WebSocket ao grupo de notificações
        async_to_sync(self.channel_layer.group_add)(
            'main',
            self.channel_name
        )
        self.groups.append('main')
    
    def disconnect(self, close_code):
        # Remove o WebSocket do grupo de notificações
        async_to_sync(self.channel_layer.group_discard)(
            'main',
            self.channel_name
        )

    def receive(self, text_data):
        # Carrega a mensagem JSON recebida do WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message", "")  # Pegue o campo "message" da mensagem recebida
        user = text_data_json.get('user',"")
        number =text_data_json.get('number')
        send = text_data_json.get('send',False)

        print(f"Mensagem recebida: {message}")


        if send:
            _headers = {
                'Authorization': f'Bearer {settings.TOKEN_ACESS}',
                'Content-Type':'application/json' 
            }

            url = f'https://graph.facebook.com/v21.0/{settings.NUMBER_ID}/messages'
            json_data= {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text":{
                    "body":message,
                }
            }
            data = json.dumps(json_data)
            response = requests.post(url, headers=_headers,data=data)

        try:
            async_to_sync(self.channel_layer.group_send)(
                "main",
                {
                    'type': 'main_message',  # O 'type' deve mapear para o método 'main_message'
                    'user':user,
                    "number":number,
                    'message': message
                }
            )
            print("Mensagem enviada para o grupo")
        except Exception as e:
            print(f"Erro ao enviar a mensagem para o grupo: {e}")

    def main_message(self, event):
        # Obtém a mensagem do evento
        message = event.get('message', '')
        user = event.get('user','')
        number = event.get('number','')

        print(f"Mensagem recebida no grupo: {message}")
        
        # Envia a mensagem de volta ao WebSocket
        self.send(text_data=json.dumps({
            'user':user,
            'number':number,
            'message': message,
        }))
