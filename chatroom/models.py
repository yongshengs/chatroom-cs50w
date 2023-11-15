from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
import os


def profile_picture_path(instance, filename):
    """
    Generate file path for profile picture
    """
    _, file_extension = os.path.splitext(filename)
    # Rename the file to a unique name
    new_filename = f"{uuid4().hex}{file_extension}"
    return f"users/{instance.username}/{new_filename}"


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=120, blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_path, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'chat_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
 

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms')
    members = models.ManyToManyField(User, related_name='chats')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_rooms'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f"Chat #{self.id} Owner: {self.owner.username} & Member: {self.members.first().username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.content} by {self.sender} to {self.receiver} on {self.timestamp.strftime('%d %b %Y %I:%M:%S %p')}"
    
    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-timestamp']

    def get_chat_list(u):
        all_messages = Message.objects.filter(models.Q(receiver=u) | models.Q(sender=u)).order_by('-timestamp')
        latest_chats = []

        for message in all_messages:
            to_me = message.receiver == u
            from_me = message.sender == u
            if to_me or from_me:
                if to_me:
                    other_user = message.sender
                else:
                    other_user = message.receiver

                if other_user not in [chat.sender if chat.sender != u else chat.receiver for chat, _ in latest_chats]:
                    latest_chats.append((message, message.chat.id))

        return latest_chats