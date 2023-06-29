from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm

def homePage(request):
    return render(request, "accounts/homePage.html")


def signup(request):
    form = SignupForm()
    return render(request, "accounts/signup.html", {"form":form})