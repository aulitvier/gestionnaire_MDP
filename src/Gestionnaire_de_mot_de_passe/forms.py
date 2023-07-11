from datetime import datetime
from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(min_length=12, widget=forms.PasswordInput())
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'])

    # Vérifier la présence de lettres minuscules, majuscules, chiffres et caractères spéciaux (@$!%*?&) dans le mot de passe et qui fasse au moins 12 caractères 
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) >= 12:
            if re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", password):
                return password
            else:
                raise forms.ValidationError("Le mot de passe doit contenir au moins une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.")
        else:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 12 caractères.")
    
    # vérifie que l'email a la syntaxe suivante : monmail@orange.fr
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        else:
            print("else")
            raise forms.ValidationError("Adresse e-mail invalide.")
    
    # vérifie que la date de naissance a la syntaxe suivante : 01/07/2021
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get("birthdate")
        birthdate = str(birthdate)
        try:
            birthdate_str = datetime.strptime(birthdate, "%Y-%m-%d")
            return birthdate_str
        except ValueError:
            raise forms.ValidationError("Format de date invalide. Veuillez écrire la date dans la syntaxe suivante : JJ/MM/AAAA")
        


# class SignupForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = ('email', 'password', 'last_name', 'first_name', 'birthdate')

#     def clean_password(self):
#             password = self.cleaned_data.get("password")
#             if len(password) >= 12:
#                 if re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", password):
#                     return password
#                 else:
#                     raise forms.ValidationError("Le mot de passe doit contenir au moins une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.")
#             else:
#                 raise forms.ValidationError("Le mot de passe doit contenir au moins 12 caractères.")
        
#         # vérifie que l'email a la syntaxe suivante : monmail@orange.fr
#     def clean_email(self):
#         email = self.cleaned_data.get("email")

#         if re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             return email
#         else:
#             print("else")
#             raise forms.ValidationError("Adresse e-mail invalide.")
    
#     # vérifie que la date de naissance a la syntaxe suivante : 01/07/2021
#     def clean_birthdate(self):
#         birthdate = self.cleaned_data.get("birthdate")
#         birthdate = str(birthdate)
#         try:
#             birthdate_str = datetime.strptime(birthdate, "%Y-%m-%d")
#             return birthdate_str
#         except ValueError:
#             raise forms.ValidationError("Format de date invalide. Veuillez écrire la date dans la syntaxe suivante : JJ/MM/AAAA")



# class LoginForm(forms.Form):
#         email = forms.EmailField(max_length=50)
#         password = forms.CharField(min_length=12, widget=forms.PasswordInput())
