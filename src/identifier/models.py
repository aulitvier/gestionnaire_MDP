from django.db import models

from user.models import customUser

class Username(models.Model):

    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)