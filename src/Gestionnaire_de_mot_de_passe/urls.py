from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from identifier.views import IdentifierView, TemplateIdentifierView, DisplayUsernameView, UsernameDeleteView, UsernameUpdateView
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),# url pour s'inscrire
    path('account/', include(('django.contrib.auth.urls', 'auth_app'), namespace='auth_app')),  # url pour se connecter
    path('accounts/profile/', views.HomePageLoginView.as_view(), name="homepage"), # url aprés connexion
    path('account/logout/', views.IndexView.as_view()),
    path('username/display/', login_required(DisplayUsernameView.as_view()), name='username_display'),
    path('username/update/<int:pk>/', login_required(UsernameUpdateView.as_view()), name='username_update'),
    path('username/delete/<int:pk>/', UsernameDeleteView.as_view(), name='username_delete'),
    path('testform/', login_required(IdentifierView.as_view())),
    path('testform/create-username-success', login_required(TemplateIdentifierView.as_view())),
    # path('generate/', views.generatePassword)


    ]
