from django.urls import include, path
from django.contrib.auth.decorators import login_required

from identifier.views import (IdentifierView, TemplateIdentifierView, DisplayUsernameView, UsernameDeleteView,
                              UsernameUpdateView)
from user.views import SignupView, HomePageLoginView, IndexView, CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view()),  # url pour s'inscrire
    # path('account/', include(('django.contrib.auth.urls', 'auth_app'), namespace='auth_app')),  # url pour se connecter
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', HomePageLoginView.as_view(), name="homepage"),  # url aprés connexion
    path('account/logout/', IndexView.as_view()),
    path('username/display/', login_required(DisplayUsernameView.as_view()), name='username_display'),
    path('username/update/<int:pk>/', login_required(UsernameUpdateView.as_view()), name='username_update'),
    path('username/delete/<int:pk>/', login_required(UsernameDeleteView.as_view()), name='username_delete'),
    path('create/username/', login_required(IdentifierView.as_view())),
    path('create/username/create-username-success', login_required(TemplateIdentifierView.as_view())),

    ]
