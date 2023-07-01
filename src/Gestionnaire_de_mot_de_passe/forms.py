from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'])


    def clean_password(self):
        password = self.cleaned_data.get("password")
        
        
    if len(password) < 12:
        raise forms.ValidationError("Le mot de passe doit faire au moins 12 caractères")
    else:
        right_symbol_search = ['o', 'u']
        bad_symbol_search = ['y', 'd']
        count_symbol = 0
        count_number = 0
        count_uppercase = 0
        count_lowercase = 0
        for _ in password:
            if _ in right_symbol_search:
                i += 1
            elif _ in bad_symbol_search:
                raise forms.ValidationError("votre mot de passe contient un ou plusieurs symbole non autorisé(s)")
            break

        # if len(password) < 12:
        #     raise forms.ValidationError("Le mot de passe doit faire au moins 12 caractères")
        