from django.db import models
from auth_app.models import Users,Base


class Chats(Base):
  
  sent_by = models.ManyToManyField(Users, related_name='sended_messages')
  sent_to = models.ManyToManyField(Users, related_name='recieved_message')
  message = models.TextField()
  is_read = models.BooleanField(default = False)
  sent_time = models.DateTimeField(auto_now_add = True)
  
  
class ChatActivity(Base):
  
  user_1 = models.ManyToManyField(Users,related_name='con1')
  user_2 = models.ManyToManyField(Users,related_name='con2')
  timestamp = models.DateTimeField(auto_now_add = True)
  room_id = models.CharField(max_length = 100,default = None)
  

  
  

  
  