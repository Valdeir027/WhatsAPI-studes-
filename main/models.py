from django.db import models
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=500)
    wa_id = models.CharField(max_length=255)


    def __str__(self) -> str:
        return f"{self.wa_id}"

class Chat(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.profile.wa_id}"
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING, related_name='chat_messages')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    message_id  = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()
    text = models.TextField()


    @staticmethod
    def timestap_from_data(timestamp:str):
        return datetime.fromtimestamp(int(timestamp))
    
    def __str__(self) -> str:
        return f"{self.text[:15]}:{self.profile.wa_id}"
    
