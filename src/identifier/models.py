from django.apps import apps
from django.db import models
from user.models import customUser
from django.utils.crypto import pbkdf2
from django.utils.crypto import get_random_string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Username(models.Model):
    
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)


class Password_storage(models.Model):
    nonce = models.BinaryField()
    encrypted_key = models.BinaryField()
    tag = models.BinaryField()


class Login_informations(models.Model):
    
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    Username_id = models.ForeignKey(Username, on_delete=models.CASCADE)
    password = models.TextField()
    website_name = models.CharField(max_length=255)
    password_storage = models.ForeignKey(Password_storage, on_delete=models.CASCADE)



# class Session(models.Model):
#     User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
#     derived_key = models.TextField()