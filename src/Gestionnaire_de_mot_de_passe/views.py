from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm
from user.models import SignupUser


def homePage(request):
    return render(request, "accounts/homePage.html")


def signup(request):
    form = SignupForm()
    if request.method == "POST": # vérifie la méthode
        form = SignupForm(request.POST) # récupère les données du formulaire sous forme d'un dictionnaire
        if form.is_valid(): # valide ou non les données
            form = form.cleaned_data # convertie les données de html en python
            create_user = SignupUser(
                email = form["email"],
                password = form["password"],
                lastName = form["last_name"],
                firstName = form["first_name"],
                birthDate = form["birthdate"])
            create_user.save()
            print(form)
    
    return render(request, "accounts/signup.html", {"form":form})