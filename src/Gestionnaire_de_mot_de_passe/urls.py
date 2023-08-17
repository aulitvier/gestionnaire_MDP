"""
URL configuration for Gestionnaire_de_mot_de_passe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from identifier.views import IdentifierView, TemplateIdentifierView, DisplayUsernameView, UsernameDeleteView, UsernameUpdateView
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),# url pour s'inscrire
    path('account/', include(('django.contrib.auth.urls', 'admin'), namespace='admin')), # url pour se connecter
    path('accounts/profile/', views.homePageLogin, name="homepage"), # url aprés connexion
    path('account/logout/', views.index),
    # path('username/create/', UsernameCreateView.as_view()),
    # path('username/create/create-username-success', TemplateUsernameView.as_view()),
    # path('username/display/', DisplayUsernameView.as_view(), name='username_display'),
    # path('username/update/<int:pk>/', UsernameUpdateView.as_view(), name='username_update'),
    # path('username/delete/<int:pk>/', UsernameDeleteView.as_view(), name='username_delete'),
    path('testform/', IdentifierView.as_view()),
    path('testform/create-username-success', TemplateIdentifierView.as_view()),


    ]
