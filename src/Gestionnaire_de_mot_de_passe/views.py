from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm
from django.core.exceptions import ObjectDoesNotExist

from user.models import customUser


def homePageLogin(request):
    return HttpResponse(f"Bienvenu {request.user.first_name}")


def signup(request):
        form = SignupForm()
        if request.method == "POST": # vérifie la méthode
            form = SignupForm(request.POST) # récupère les données du formulaire sous forme d'un dictionnaire
            if form.is_valid(): # valide ou non les données
                form = form.cleaned_data # convertie les données de html en python
            # création de l'utilisateur dans la BDD*
                try : # regarde si l'adresse email n'est pas déjà présent dans la base de données
                    customUser.objects.get(email=form['email'])
                    form = SignupForm()
                    return render(request, "accounts/signup.html", {"form":form})
                
                except ObjectDoesNotExist: # si l'adresse email n'existe pas, j'enregistre l'utilisateur dans la base de données
                    print(form)
                    registration_user = customUser.objects.create_user(email=form["email"], password=form["password"], last_name=form["last_name"], first_name=form["first_name"], birthdate=form["birthdate"])
        
        return render(request, "accounts/signup.html", {"form":form})