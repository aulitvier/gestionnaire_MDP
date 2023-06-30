from django.db import models

# Create your models here.
class SignupUser(models.Model):
    email = models.CharField(max_length=50)
    password = models.TextField()
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    birthDate = models.DateField()
    premium = models.BooleanField(default=False)