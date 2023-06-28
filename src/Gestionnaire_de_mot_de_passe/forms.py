from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(min_length=8, widget=forms.HiddenInput())
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'])
    