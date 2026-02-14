from django.urls import path
from . import views
from .views import (
    listeEmployes,
    ajouterEmployes,
    modifierEmployes,
    supprimerEmployes
)

urlpatterns = [
    path('', views.index, name='index'),
    path('employe/', views.listeEmployes.as_view()),
    path('employe/ajouter/', views.ajouterEmployes.as_view()),
    path('employe/modifier/<int:id>/', views.modifierEmployes.as_view()),
    path('employe/supprimer/<int:id>/', views.supprimerEmployes.as_view())
]
