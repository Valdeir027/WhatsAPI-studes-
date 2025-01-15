from django.shortcuts import render

# DRF imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from main.consumers import MainConsumer
from main.models import *
from django.conf import settings
#channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class WebHook(APIView):
    permission_classes = [AllowAny]


    def post(self, requests):
        data = requests.data
        print(data)
        channel_layer = get_channel_layer()
        try:
            sts = data["entry"][0]["changes"][0]["value"]['statuses']
        except:
            try:
                user = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
            except:
                user = "bot"
            numero = data["entry"][0]["changes"][0]["value"]["contacts"][0]['wa_id']
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]

            perfil, _ = Profile.objects.get_or_create(name= user, wa_id=numero)
            if perfil.wa_id != settings.NUMBER_ID:
                chat_obj, _ = Chat.objects.get_or_create(profile= perfil)

            if perfil:
                message_obj, _  = Message.objects.get_or_create(profile=perfil,message_id=message['id'],timestamp=Message.timestap_from_data(message['timestamp']),text=message['text']['body'], chat=chat_obj) # type: ignore

                if message_obj:
                    async_to_sync(channel_layer.group_send)(
                        "main",  # Nome do grupo
                        {
                            "type": "main_message",  
                            'user': message_obj.profile.name,
                            'number':message_obj.chat.profile.wa_id,
                            "message": message_obj.text,
                        }
                    )

        return Response(status=200)

    def get(self, requests):
        # Para o método GET, obtenha os parâmetros de consulta
        query_params = requests.query_params
        print(query_params)
        # Você pode acessar parâmetros individuais assim:
        hub_mode = query_params.get('hub.mode')
        hub_challenge = query_params.get('hub.challenge')
        hub_verify_token = query_params.get('hub.verify_token')

        print(hub_challenge)
        return Response(int(hub_challenge))