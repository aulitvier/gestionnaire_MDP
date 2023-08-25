# import json
# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import Signal, receiver
# from django.utils import timezone
# import logging

# logger = logging.getLogger(__name__)



# session_started = Signal()


# # @receiver(user_logged_in)
# # def record_session_start(sender, request, user, **kwargs):
# #     start_session_user = request.session['session_start_time'] = timezone.now()
# #     json.dumps(start_session_user, default=str)


# @receiver(user_logged_in)
# def user_logged_in_callback(sender, request, user, **kwargs):
#     start_session_user = timezone.now()

#     # Sérialiser la chaîne de caractères en JSON
#     start_session_user_json = json.dumps(start_session_user, default=str)

#     # Enregistrer la chaîne JSON dans la session
#     request.session['session_start_time'] = start_session_user_json
#     print(f"Session started for user {user.email}")