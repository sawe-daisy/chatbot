from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models.fields import DateTimeField
from django.utils.translation import ugettext as _

# Create your models here.

class User(AbstractUser):
    """Default user for VeritasAI Engine."""

    #: First and last name do not cover name patterns around the globe
    username = CharField(null=True,max_length=255, unique=True)
    first_name = CharField(null=True,max_length=255, unique=False)
    last_name = CharField(null=True,max_length=255, unique=False)
    email_address = CharField(blank=True, null=True,max_length=255)

    def __str__(self):
        return self.username
    
    # def save(self):
    #     super().save()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(username__icontains=name).all()

class Chatbot(models.Model):
    # chat= CharField( null=True,max_length=256, unique=False)
    title= CharField( null=True,max_length=256, unique=False)
    user=models.ManyToManyField(User, related_name='name')

    def __str__(self) -> str:
        return self.title

    def connect_user(self, user):
        is_user_added =False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added=True
        elif user in self.users.all():
            is_user_added=True
        return is_user_added
    
    def disconnect_user(self, user):
        is_user_removed= True
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed=True
        return is_user_removed

    @property
    def group_name(self):
        return f"Chatroom-{self.id}"
        
class ChatManager(models.Manager):
    def room(self, room):
        chats= Chats.objects.filter(room= room).order_by("-time")
        return chats


class Chats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    time = DateTimeField(auto_now=True)
    content = models.TextField(unique=False, blank=False)

    objects= ChatManager()

    def __str__(self):
        return self.content

