from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from identifier.forms import LoginInformationsForm, UsernameForm
from identifier.models import Login_informations, Username
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
 
class LoginInformationView(InlineFormSetFactory):  # classe inline de IdentifierView
    model = Login_informations  # nom du model
    form_class = LoginInformationsForm  # nom de la classe
    factory_kwargs = {'extra': 2, 'max_num': 1, 'can_order': False, 'can_delete': False}
    # permet d'enlever le bouton "supprimer" et d'affiche'r le formulaire qu'une fois


class IdentifierView(CreateWithInlinesView):
    model = Username
    inlines = [LoginInformationView]  # vue du formulaire enfant
    form_class = UsernameForm
    template_name = "identifier_manage/create_identifier.html"

    def forms_valid(self, form, inlines):
        user_id = self.request.user  # récupère les données du formulaire
        value_already_exists = Username.objects.filter(User_id=user_id, username=self.request.POST["username"])
        # vérifie si l'username existe déjà
        if value_already_exists:
            form.add_error("username", "l'identifiant existe déjà")
            # envoie le message d'erreur dans le champ username
            return self.forms_invalid(form, inlines)
        else:
            form.instance.User_id = user_id  # jointure entre User_id de Username et l'id de customUser
            for formset in inlines:  # permet de récupérer chaque liste du formulaire
                for form2 in formset:
                    # data_copy = form2.cleaned_data()
                    password_value = form2.cleaned_data.get("password")
                    # Encoder et chiffrer le mot de passe
                    encodeddata = password_value.encode("utf-8")
                    key = get_random_bytes(
                        16)  # Assurez-vous de sauvegarder cette clé pour le déchiffrement ultérieur
                    cipher = AES.new(key, AES.MODE_EAX)
                    cipherpassword, tag = cipher.encrypt_and_digest(encodeddata)

                    # Remplacer le mot de passe par le mot de passe chiffré

                    # Réinstancier le formulaire avec le mot de passe chiffré (si nécessaire)

                    login_form = form2.save(commit=False)
                    login_form.password = cipherpassword
                    login_form.User_id_id = user_id.id
                    # jointure entre User_id_id de login_informations et l'id de customuser
                    login_form.Username_id = form.instance.id
                        # jointure entre username_id de login_information et l'id d'username
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
    model = Login_informations
    template_name = "identifier_manage/display_usernames.html"

    def get_queryset(self):
        # Récupérer l'ID de l'utilisateur connecté
        user_id = self.request.user.id

        # Filtrer les articles dont l'auteur a le même ID que l'utilisateur connecté
        queryset = Login_informations.objects.filter(User_id=user_id)
        return queryset
    
    
class UsernameUpdateView(UpdateWithInlinesView):
    model = Username
    inlines = [LoginInformationView]
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
