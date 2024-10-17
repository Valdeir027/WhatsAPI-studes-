from django.shortcuts import render

# DRF imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny



class WebHook(APIView):

    def post(self, requests):
        data = requests.data

        print(data)

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