from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'])
