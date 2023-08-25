from django.apps import apps
from django.db import models
from user.models import customUser
from django.utils.crypto import pbkdf2
from django.utils.crypto import get_random_string

class Username(models.Model):
    
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)

class Login_informations(models.Model):
    
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    Username_id = models.ForeignKey(Username, on_delete=models.CASCADE)
    password = models.TextField()
    website_name = models.CharField(max_length=255)
    # permet de chiffrer le mot de passe
    # def save(self, *args, **kwargs):
    #     if self.password and not self.password.startswith('pbkdf2'):
    #         salt = get_random_string(length=32)
    #         self.password = pbkdf2(self.password.encode('utf-8'), salt.encode('utf-8'), iterations=10000, dklen=128)
    #     super().save(*args, **kwargs)





