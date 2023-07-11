from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# class SignupUser(models.Model):
#     email = models.CharField(max_length=50, unique=True)
#     password = models.TextField()
#     lastName = models.CharField(max_length=50)
#     firstName = models.CharField(max_length=50)
#     birthDate = models.DateField()
#     premium = models.BooleanField(default=False)



class MyUserManager(BaseUserManager):
    def create_user(self, email, password, last_name, first_name, birthdate):
        if not email:
            raise ValueError("Vous devez rentrer une adresse email")
        
        user = self.model(
            email=self.normalize_email(email),
            last_name = last_name,
            first_name = first_name,
            birthdate = birthdate
        )
        user.set_password(password)

        user.save()
        return user

# CREER AVEC ABSTRACTBASEUSER PLUTOT DONC SUPPRIMER SCHEMA, TABLE, MIGRATION  
class customUser(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True, blank=False)
    username = None

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    premium = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name", "birthdate"]
    objects = MyUserManager()

    def has_perm(self, perm, objet=None):
        return True

    def has_module_perms(self, app_label):
        return True