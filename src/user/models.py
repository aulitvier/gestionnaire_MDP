from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MyUserManager(BaseUserManager):
    def create_user(self, email, password, last_name, first_name, birthdate): # paramètre pour créer un utilisateur
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

class customUser(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True, blank=False)
    username = None

    is_active = models.BooleanField(default=True) # si l'utilisateur est actif
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) # s'il est admin
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    premium = models.BooleanField(default=False)

    USERNAME_FIELD = "email" # chammps avec lequel je souhaite que l'utilisateur s'identifit
    REQUIRED_FIELDS = ["last_name", "first_name", "birthdate"]
    objects = MyUserManager()

    def has_perm(self, perm, objet=None):
        return True

    def has_module_perms(self, app_label):
        return True