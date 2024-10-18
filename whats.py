import abc
import requests
import json

from constance import settings


class Whats():
    _headers = {
        'Authorization': f'Bearer {settings.TOKEN_ACESS}',
        'Content-Type':'application/json' 
    }
    
    def send_hello_world(self,number:str):
        url = f'https://graph.facebook.com/v21.0/{settings.NUMBER_ID}/messages'
        json_data= {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                "code": "en_US"
                }
            }
        }
        data = json.dumps(json_data)
        response = requests.post(url, headers=self._headers,data=data)

        return response.json()

    

