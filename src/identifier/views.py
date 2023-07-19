from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView

# Create your views here.

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import customUser, Username
from .forms import UsernameForm


@method_decorator(login_required(login_url="/account/login"), name="post")
class UsernameCreateView(CreateView):
    model = Username # défini le modele à utiliser
    template_name = "identifier_manage/username.html" # défini le chemin du template
    form_class = UsernameForm # défini le formulaire
    
    def form_valid(self, form):
        if form.is_valid(): # si le formulaire est valide
            username_id = self.request.user # récupère les données du formulaire
            value_already_exists = Username.objects.filter(User_id=username_id, username=self.request.POST["username"]) # vérifie si l'username existe déjà
            if value_already_exists:
                form.add_error("username", "l'identifiant existe déjà") # envoie le message d'erreur dans le champ username
                return self.form_invalid(form)
            else :
                form.instance.User_id = username_id # jointure entre l'id de customUser et User_id de Username
                return super().form_valid(form) # enregistre le formulaire
    
    def form_invalid(self, form):
        # Le formulaire n'est pas valide, afficher le formulaire avec les erreurs
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return "create-username-success"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Modifier"
        return context


class TemplateUsernameView(TemplateView):
    template_name = "identifier_manage/success_username_create.html"


class DisplayUsernameView(ListView):
    model = Username
    template_name = "identifier_manage/display_usernames.html"

    def get_queryset(self):
        # Récupérer l'ID de l'utilisateur connecté
        user_id = self.request.user.id

        # Filtrer les articles dont l'auteur a le même ID que l'utilisateur connecté
        queryset = Username.objects.filter(User_id=user_id)
        return queryset
    

@method_decorator(login_required(login_url="/account/login"), name="post")
class UsernameUpdateView(UpdateView):
    model = Username
    template_name = "identifier_manage/username.html"
    fields = ['username']  # Les champs que vous souhaitez modifier dans le formulaire
    success_url = reverse_lazy('username_display')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Modifier"
        return context