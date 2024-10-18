from django.shortcuts import render

# DRF imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from main.consumers import MainConsumer

#channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class WebHook(APIView):
    permission_classes = [AllowAny]

    def post(self, requests):
        data = requests.data

        channel_layer = get_channel_layer()

        # Envia a mensagem para o grupo 'chat'
        async_to_sync(channel_layer.group_send)(
            "main",  # Nome do grupo
            {
                "type": "main_message",  # Esse "type" corresponde ao método 'chat_message' no consumer
                'user': data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"],
                'number':"",
                "message": data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
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