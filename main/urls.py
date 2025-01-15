from django.urls import path 
from . import views

urlpatterns =[
    path('', views.index),
    path('send_message',views.send_message),
    path('<str:wa_id>',views.list_messages),
]