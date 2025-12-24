from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_employes, name='liste_employes'),
    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('modifier/<int:id>/', views.modifier_employe, 
         name='modifier_employe'),
    path('supprimer/<int:id>/', views.supprimer_employe, 
         name='supprimer_employe')
]