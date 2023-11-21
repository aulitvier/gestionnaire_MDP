from os import urandom
from django.shortcuts import render
from django.urls import reverse_lazy
from Gestionnaire_de_mot_de_passe.forms import SignupForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from user.models import customUser
from django.views.generic.edit import FormView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from django.contrib.auth import get_user_model
from base64 import b64encode, b64decode


@method_decorator(login_required, name='dispatch')
class HomePageLoginView(View):
    template_name = "accounts/homePageLogin.html"  # après la connexion

    def get(self, request):
        form = request.user.first_name
        return render(request, self.template_name, {"form": form})


class IndexView(TemplateView):
    template_name = "index.html"  # Template de logout


class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        # Cette méthode est appelée lorsque le formulaire est valide
        try:
            customUser.objects.get(email=form.cleaned_data['email'])
            # Si l'utilisateur existe déjà, réenvoie le formulaire
            return self.render_to_response(self.get_context_data(form=form))
        except ObjectDoesNotExist:  # si l'objet n'existe pas créer l'utilisateur
            salt = urandom(16)  # création d'un sel aléatoire
            encoded_salt = b64encode(salt).decode('utf-8')  # transforme le sel en bytes
            customUser.objects.create_user(  # création de l'utilisateur
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                last_name=form.cleaned_data["last_name"],
                first_name=form.cleaned_data["first_name"],
                birthdate=form.cleaned_data["birthdate"],
                salt=encoded_salt
            )
            return super().form_valid(form)

    def form_invalid(self, form):
        # Cette méthode est appelée lorsque le formulaire n'est pas valide
        return self.render_to_response(self.get_context_data(form=form))


class CustomLoginView(LoginView):

    def form_valid(self, form):
        #  Récupére le mot de passe saisi par l'utilisateur en clair
        main_password = form.cleaned_data.get("password")
        username = form.cleaned_data.get("username")

        # Récupére l'utilisateur sans l'authentifier pour accéder à son sel
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            salt = user.salt
            decode_salt = b64decode(salt)

        except User.DoesNotExist:
            # si l'utilisateur n'existe pas
            return super().form_invalid(form)

        # généreration de la clé dérivée
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # algorithme de hashage
            length=32,  # taille en bytes
            salt=decode_salt,  # sel
            iterations=100000,
            backend=default_backend()  # retourne le backend en cours
        )
        derived_key = base64.urlsafe_b64encode(kdf.derive(main_password.encode()))
        derived_key_str = derived_key.decode('utf-8')  # transforme la clé en chaine de caractère
        self.request.session['derived_key'] = derived_key_str  # stocke la clé dérivée dans la session
        print(derived_key_str)

        # après, Django gérer l'authentification
        auth_user = authenticate(self.request, username=username, password=main_password)

        if auth_user is not None:
            login(self.request, auth_user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
