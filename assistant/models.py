from django.db import models
from userschema.models import CustomUser

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100, unique=True)
    conversation = models.JSONField(blank = True, null = True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.title}'