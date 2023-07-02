from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm

def homePage(request):
    return render(request, "accounts/homePage.html")


def signup(request):

    if request.method == "POST": # vérifie la méthode
        form = SignupForm(request.POST) # récupère les données du formulaire sous forme d'un dictionnaire
        if form.is_valid(): # valide ou non les données
            print(form.cleaned_data) # convertie les données de html en python
    
    return render(request, "accounts/signup.html", {"form":form})