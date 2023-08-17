from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from extra_views import CreateWithInlinesView, InlineFormSetFactory
from identifier.forms import LoginInformationsForm, UsernameForm
from identifier.models import Login_informations, Username
from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

 
class LoginInformationView(InlineFormSetFactory): # classe inline de IdentifierView
    model = Login_informations # nom du model
    form_class = LoginInformationsForm # nom de la classe
    factory_kwargs = {'extra': 2, 'max_num': 1, 'can_order': False, 'can_delete': False} # permet d'enlever le bouton "supprimer" et d'affiche'r le formulaire qu'une fois

@method_decorator(login_required(login_url="/account/login"), name="post")
class IdentifierView(CreateWithInlinesView):
    model = Username
    inlines = [LoginInformationView]
    form_class = UsernameForm
    template_name = "identifier_manage/testaffiche.html"

    def forms_valid(self, form, inlines):
                user_id = self.request.user # récupère les données du formulaire
                value_already_exists = Username.objects.filter(User_id=user_id, username=self.request.POST["username"]) # vérifie si l'username existe déjà
                if value_already_exists:
                    form.add_error("username", "l'identifiant existe déjà") # envoie le message d'erreur dans le champ username
                    # RENVOYER LES DEUX FORMS
                    return self.forms_invalid(form, inlines)
                else :
                    form.instance.User_id = user_id # jointure entre User_id de Username et l'id de customUser
                    for formset in inlines: # permet de récupérer chaque liste du formulaire
                        for form2 in formset:
                            login_form = form2.save(commit=False)
                            login_form.User_id_id = user_id.id # jointure entre User_id_id de login_informations et l'id de customuser
                            login_form.Username_id = form.instance.id # jointure entre username_id de login_information et l'id d'username
                    return super().forms_valid(form, inlines)

        
    def form_invalid(self, form):
        # Le formulaire n'est pas valide, afficher le formulaire avec les erreurs
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return "create-username-success"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Créer"
        return context

class TemplateIdentifierView(TemplateView):
    template_name = "identifier_manage/success_identifier_create.html"




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
    

class UsernameDeleteView(DeleteView):
    model = Username
    template_name = "identifier_manage/username_delete.html"
    success_url = reverse_lazy('username_display')
