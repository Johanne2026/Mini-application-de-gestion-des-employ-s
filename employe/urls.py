from django.contrib import admin
from django.urls import path
from . import views
from .views import listeEmployes, ajouterEmployes, modifierEmployes, supprimerEmployes

# urlpatterns = [
#    path('', views.liste_employes, name='liste_employes'),
#    path('ajouter/', views.ajouter_employe, name='ajouter_employe'),
#    path('modifier/<int:id>/', views.modifier_employe, 
#         name='modifier_employe'), <int:id>/
#    path('supprimer/<int:id>/', views.supprimer_employe, 
#         name='supprimer_employe')
# ]

urlpatterns = [
    path('employe/', views.listeEmployes.as_view()),
    path('employe/ajouter/', views.ajouterEmployes.as_view()),
    path('employe/modifier/<int:id>/', views.modifierEmployes.as_view()),
    path('employe/supprimer/<int:id>/', views.supprimerEmployes.as_view())

]