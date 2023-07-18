from django import forms

from identifier.models import Username





# class UsernameForm(forms.Form):
#     username = forms.CharField(max_length=255)

class UsernameForm(forms.ModelForm):
    class Meta:
        model = Username
        fields = ["username"]