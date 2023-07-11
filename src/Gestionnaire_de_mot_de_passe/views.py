from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm
# from user.models import SignupUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from user.models import MyUserManager, customUser


def homePageLogin(request):
    return HttpResponse(f"{request.user.email}")


def signup(request):
        form = SignupForm()
        if request.method == "POST": # vérifie la méthode
            form = SignupForm(request.POST) # récupère les données du formulaire sous forme d'un dictionnaire
            if form.is_valid(): # valide ou non les données
                form = form.cleaned_data # convertie les données de html en python
            # création de l'utilisateur dans la BDD*
                try :
                    customUser.objects.get(email=form['email'])
                    form = SignupForm()
                    return render(request, "accounts/signup.html", {"form":form})
                
                except ObjectDoesNotExist:
                    print(form)
                    registration_user = customUser.objects.create_user(email=form["email"], password=form["password"], last_name=form["last_name"], first_name=form["first_name"], birthdate=form["birthdate"])
        
        return render(request, "accounts/signup.html", {"form":form})

def login(request):
    form = form
    return render(request, "accounts/login.html", {"form":form})
#     form = LoginForm()
#     if request.method == "POST": # vérifie la méthode
#         form = LoginForm(request.POST) # récupère les données du formulaire sous forme d'un dictionnaire
#         if form.is_valid(): # valide ou non les données
#             form = form.cleaned_data # convertie les données de html en python
#             email  = form["email"]
#             # email = email.strip()
#             password = form["password"]
#             # password = password.strip()
#             try_login = authenticate(request, username=email, password=password)
#             print(email + "\n")
#             print(password)
#             print(try_login)
            
#     return render(request, "accounts/login.html", {"form":form})