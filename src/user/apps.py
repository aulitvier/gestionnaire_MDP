from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in



# class UserConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'user'

#     def ready(self):
#         import user.signals  # Importez vos gestionnaires de signaux ici





# class YourAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'user'

#     def ready(self):
#         import user.signals  # Importez vos gestionnaires de signaux ici

#         # Lier le gestionnaire de signal à user_logged_in
#         user_logged_in.connect(record_session_start, sender=customUser)