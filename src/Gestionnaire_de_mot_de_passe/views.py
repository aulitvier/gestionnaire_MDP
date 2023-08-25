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


@method_decorator(login_required, name='dispatch')
class HomePageLoginView(View):
    template_name = "accounts/homePageLogin.html"

    def get(self, request, *args, **kwargs):
        form = request.user.email
        return render(request, self.template_name, {"form": form})


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Cette méthode est appelée lorsque le formulaire est valide.
        try:
            customUser.objects.get(email=form.cleaned_data['email'])
            # Si l'utilisateur existe déjà, réaffichez le formulaire.
            return self.render_to_response(self.get_context_data(form=form))
        except ObjectDoesNotExist:
            registration_user = customUser.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                last_name=form.cleaned_data["last_name"],
                first_name=form.cleaned_data["first_name"],
                birthdate=form.cleaned_data["birthdate"]
            )
            return super().form_valid(form)

    def form_invalid(self, form):
        # Cette méthode est appelée lorsque le formulaire n'est pas valide.
        return self.render_to_response(self.get_context_data(form=form))