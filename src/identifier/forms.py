from django import forms
from django.forms import inlineformset_factory

from identifier.models import Login_informations, Username


class UsernameForm(forms.ModelForm):
    class Meta:
        model = Username
        fields = ["username"]


class LoginInformationsForm(forms.ModelForm):
    class Meta:
        model = Login_informations
        fields = ["password", "website_name"]
