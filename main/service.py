import simplejson
import requests

from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_whats_message(number, message):
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
    data = simplejson.dumps(json_data)

    response = requests.post(url, headers=_headers,data=data)
    print(response)
    return response


def send_websocket_message(message_obj):
    print("está dando certo?")

    print(message_obj.chat.profile.wa_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "main",  # Nome do grupo
        {
            "type": "main_message",  
            'user': message_obj.profile.name,
            'number':message_obj.chat.profile.wa_id,
            "message": message_obj.text,
        }
    )
