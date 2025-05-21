from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)  # nuevo campo
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.sender} a {self.receiver}: mensaje({self.content[:20]}) archivo({self.file})"
