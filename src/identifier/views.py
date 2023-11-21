from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView
from identifier.forms import LoginInformationsForm, UsernameForm
from identifier.models import Login_informations, Username, Password_storage
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import ast


class LoginInformationView(InlineFormSetFactory):  # classe inline de IdentifierView
    model = Login_informations  # nom du model
    form_class = LoginInformationsForm  # nom de la classe
    # permet d'enlever le bouton "supprimer" et d'affiche'r le formulaire qu'une fois
    factory_kwargs = {'extra': 2, 'max_num': 1, 'can_order': False, 'can_delete': False}


class IdentifierView(CreateWithInlinesView):
    model = Username
    inlines = [LoginInformationView]  # vue du formulaire enfant
    form_class = UsernameForm
    template_name = "identifier_manage/create_identifier.html"

    def forms_valid(self, form, inlines):
        user_id = self.request.user  # récupère les données de l'utilisateur
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
                    password_value = form2.cleaned_data.get("password")  # récupère le mot de passe
                    encoded_data = password_value.encode("utf-8")  # transforme le mot de passe en bytes
                    key = get_random_bytes(16)  # clé du chiffrement AES
                    cipher = AES.new(key, AES.MODE_EAX)
                    # assignation du mot de passe chiffré et du tag
                    cipherpassword, tag = cipher.encrypt_and_digest(encoded_data)
                    nonce = cipher.nonce  # creation du nonce
                    derived_key = self.request.session.get('derived_key')  # recuperation de la cle derivee
                    derived_key_bytes = derived_key.encode('utf-8')  # transoformation de la clé derivée en bytes
                    fernet = Fernet(derived_key_bytes)
                    encrypted_key = fernet.encrypt(key)  # chiffre la cle AES grace a la cle derivee
                    login_form = form2.save(commit=False)
                    # remplace le mot de passe en clair par le mot de passe chiffré
                    login_form.password = cipherpassword

                    password_storage = Password_storage.objects.create(
                                                            tag=tag,
                                                            nonce=nonce,
                                                            encrypted_key=encrypted_key
                                                        )
                    # jointure entre login_informations_password_storage et l'id de password_storage
                    login_form.password_storage_id = password_storage.id
                    # jointure entre User_id_id de login_informations et l'id de customuser
                    login_form.User_id_id = user_id.id
                    # jointure entre username_id de login_information et l'id d'username
                    login_form.Username_id = form.instance.id
            return super().forms_valid(form, inlines)

    def form_invalid(self, form):
        # Le formulaire n'est pas valide, afficher le formulaire avec les erreurs
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        # si la création de l'identifiant ce fait avec succès
        return "create-username-success"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # permet de garder le même template en changeant le text du bouton "submit"
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Créer"
        return context
    

class TemplateIdentifierView(TemplateView):
    template_name = "identifier_manage/success_identifier_create.html"


class DisplayUsernameView(ListView):
    model = Login_informations
    template_name = "identifier_manage/display_usernames.html"

    def get_queryset(self, ):
        # Récupérer l'ID de l'utilisateur connecté
        user_id = self.request.user.id

        # Filtrer les articles dont l'auteur a le même ID que l'utilisateur connecté
        queryset = Login_informations.objects.filter(User_id=user_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DisplayUsernameView, self).get_context_data(**kwargs)
        combined_data = []
        for login_info in context['login_informations_list']:
            try :
                derived_key = self.request.session['derived_key']  # récupère la clé dérivée depuis la session
                fernet = Fernet(derived_key)
                password_storage = login_info.password_storage  # récupère les données de la table password_storage
                original_key = fernet.decrypt(password_storage.encrypted_key.tobytes())  # déchiffre la clé AES
                # MODE_EAX assure l'intégralitée des données
                cipher = AES.new(original_key, AES.MODE_EAX, nonce=password_storage.nonce)
                password_bytes = ast.literal_eval(login_info.password)  # convertie le mot de passe en bytes
                tag_bytes = password_storage.tag.tobytes()  # convertie le tag en bytes
                decrypted_password = cipher.decrypt_and_verify(password_bytes, tag_bytes).decode('utf-8')
                combined_data.append({  # ajoute les données de login_info et le mot de passe dechiffre
                    'login_info': login_info,
                    'decrypted_password': decrypted_password
                })

                context['combined_data'] = combined_data
            except KeyError:
                context['error_message'] = "erreur de clé veuillez vous déconnecter et reconnecter"
                return context
        return context


class UsernameUpdateView(UpdateWithInlinesView):
    model = Username
    inlines = [LoginInformationView]
    template_name = "identifier_manage/username.html"
    fields = ['username']
    success_url = reverse_lazy('username_display')
    """ la form_valid ou form_invalid ne focntionne pas sûrement parceque la requête est mal renvoyer au serveur
    """

    def forms_invalid(self, form, inlines):
        # LES DEUX FORMS NE CONTIENT PAS D'ERREUR
        print("Erreur dans le formulaire principal :", form.errors)
        for inline_form in inlines:
            print("Erreur dans un formulaire en ligne :", inline_form.errors)
        return super().forms_invalid(form, inlines)

    def forms_valid(self, form, inlines):
        # todo trouver pourquoi les formualires sont invalides
        # TODO definir la validation du formulaire
        # todo recuperer les données envoyer du formulaire
        # todo créer un nouveau nonce, tag et clé AES
        # todo changer l'ancien mot de passe dans la BDD avec le nouveau
        # todo changer l'ancien nom du site par le nouveau
        # todo changer le tag, la cle chiffré et le nonce
        # todo enfin retourner la reponse de form_valid
        # response = super().form_valid(form, inlines)
        print("efverve")
        return super(UsernameUpdateView, self).forms_valid(form, inlines)
        # print("c'est valide super trop content")
        # for formset in inlines:
        #     for form2 in formset:
        #         print("form2 : ")
        #         print(form2)
        #

        # object_id = self.kwargs['pk'] ##### fait reference a l'id de l'objet en cours
        # login_info = Login_informations.objects.get(id=object_id) ##### récupère l'objet Login_information selon l'id
        # derived_key = self.request.session['derived_key']  # récupère la clé dérivée depuis la session
        # fernet = Fernet(derived_key) ##### ?
        # password_storage = login_info.password_storage ##### récupère le mot de passe chiffré
        # original_key = fernet.decrypt(password_storage.encrypted_key.tobytes())  # déchiffre la clé AES
        # # MODE_EAX assure l'intégralitée des données
        # cipher = AES.new(original_key, AES.MODE_EAX, nonce=password_storage.nonce)
        # password_bytes = ast.literal_eval(login_info.password)  # convertie le mot de passe en bytes
        # tag_bytes = password_storage.tag.tobytes()  # convertie le tag en bytes
        # #
        # decrypted_password = cipher.decrypt_and_verify(password_bytes, tag_bytes).decode('utf-8')
        # inlines.objects.filter(id=object_id).update(
        #         password=""
        # )
        return response



        # return context
        # print("Formulaire valide")
        # print(form.cleaned_data)
        # return super().form_valid(form)

    def get_queryset(self, ):
        # Récupérer l'ID de l'utilisateur connecté
        user_id = self.request.user.id

        # Filtrer les articles dont l'auteur a le même ID que l'utilisateur connecté
        queryset = Username.objects.filter(User_id=user_id)
        return queryset
    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # permet de garder le même template en changeant le text du bouton "submit"
    """
    get_context_data sert à afficher le tableau plus les données dans ce se dernier en déchiffrant le mot de passe 
    pour qui ne s'affiche pas chiffré
    """
    def get_context_data(self, **kwargs):
        context = super(UsernameUpdateView, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        # # context["submit_text"] = "Modifier"
        # print(context["inlines"])
        combined_data = []
        object_id = self.kwargs['pk']
        login_info = Login_informations.objects.get(id=object_id)
        #     print(self.request.session)
        derived_key = self.request.session['derived_key']  # récupère la clé dérivée depuis la session
        fernet = Fernet(derived_key)
        password_storage = login_info.password_storage
        original_key = fernet.decrypt(password_storage.encrypted_key.tobytes())  # déchiffre la clé AES
        # MODE_EAX assure l'intégralitée des données
        cipher = AES.new(original_key, AES.MODE_EAX, nonce=password_storage.nonce)
        password_bytes = ast.literal_eval(login_info.password)  # convertie le mot de passe en bytes
        tag_bytes = password_storage.tag.tobytes()  # convertie le tag en bytes
        #
        decrypted_password = cipher.decrypt_and_verify(password_bytes, tag_bytes).decode('utf-8')
        combined_data.append({  # ajoute les données de login_info et le mot de passe dechiffre
                 'login_info': login_info,
                 'decrypted_password': decrypted_password
             })
        #
        context['combined_data'] = combined_data
        return context
    

class UsernameDeleteView(DeleteView):
    model = Username
    template_name = "identifier_manage/username_delete.html"
    success_url = reverse_lazy('username_display')
