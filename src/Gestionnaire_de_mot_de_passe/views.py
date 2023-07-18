from django.http import HttpResponse
from django.shortcuts import render
from Gestionnaire_de_mot_de_passe.forms import SignupForm
from django.core.exceptions import ObjectDoesNotExist
from identifier.forms import UsernameForm
from django.contrib.auth.decorators import login_required
from identifier.models import Username
from user.models import customUser

@login_required(login_url='/account/login')
def usernamePage(request):
    message = "" # message à afficher si l'id existe ou a été crée avec succés
    username_form = UsernameForm()
    user_id = request.user # récupère les données de l'utilisateur
    get_user_id = customUser.objects.get(id=user_id.id) # récupèration de l'id de l'utilisateur
    if request.method == "POST":
        username_form = UsernameForm(request.POST)
        value_already_exists = Username.objects.filter(User_id=get_user_id, username=request.POST["username"]) # cherche l'username selon l'id de la table customUser
        if value_already_exists:
              message = "l'identifiant existe déjà"
        else:
            if username_form.is_valid():
                instance = username_form.save(commit=False) # ne sauvegarde pas le formulaire tout de suite
                instance.User_id = user_id # on définit la clé etrangère de Username par rapport à l'id récupéré avec "request.user"
                instance.save() # sauvegarde des données dans la BDD
                username_form = UsernameForm()
                message = "Votre identifiant a été créé avec succés"
    return render(request, "identifier_manage/username.html", {"username_form":username_form, "message":message})


def homePageLogin(request):
    form = request.user.email
    print(form)
    return render(request, "accounts/homePageLogin.html", {"form":form})

def index(request):
    return(request, "index.html")



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