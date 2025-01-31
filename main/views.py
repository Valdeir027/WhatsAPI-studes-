from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.conf import settings
from .models import * 
import requests
import simplejson
from datetime import datetime
from main.service import send_whats_message, send_websocket_message


# Create your views here.
def index(request):
    profiles = Chat.objects.all()
    return render(request=request, template_name='index.html', context={
        'profiles':profiles
    })


def send_message(request):
    data = simplejson.loads(request.body)
    message = data.get('message')
    number=data.get('room_id')
    
    whats_json = send_whats_message(number if number!='559591452704' else '5595991452704', message).json()
    profile = Profile.objects.get(wa_id=settings.NUMBER_ID)
    chat = Chat.objects.get(profile__wa_id = number)
    message_obj, _  = Message.objects.get_or_create(profile=profile,timestamp=datetime.now(),message_id=whats_json['messages'][0]['id'],text=message,chat=chat)
    send_websocket_message(message_obj)
    return JsonResponse({
        'success':'Message sent successfully'
    })


def list_messages(request, wa_id):
    messages = Message.objects.filter(chat__profile__wa_id= wa_id)
    return render(request,template_name='chat/chat-list-message.html', context={
        'messages':messages
    })