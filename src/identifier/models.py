from django.db import models
from user.models import customUser


class Username(models.Model):
    # model de l'identifiant
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)


class Password_storage(models.Model):
    # model pour stocker les utilitaire pour chiffrer/ déchiffrer le mot de passe
    nonce = models.BinaryField()
    encrypted_key = models.BinaryField()
    tag = models.BinaryField()


class Login_informations(models.Model):
    # model des informations de l'identifiant
    User_id = models.ForeignKey(customUser, on_delete=models.CASCADE)
    Username_id = models.ForeignKey(Username, on_delete=models.CASCADE)
    password = models.TextField()
    website_name = models.CharField(max_length=255)
    password_storage = models.ForeignKey(Password_storage, on_delete=models.CASCADE)
