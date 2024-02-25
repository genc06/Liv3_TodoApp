from Todo_App import views
from django.urls import path



urlpatterns = [
    path('', views.showIndex, name="index"),
    path('ajouter-tache/', views.ajouter_tache, name='ajouter_tache'),  # URL pour ajouter une tâche
    path('ajouter-tache-liste/', views.ajouter_tache_liste, name='ajouter_tache_liste'),
    path('modifier-tache/<int:tache_id>/', views.modifier_tache, name='modifier_tache'),  # URL pour modifier une tâche
    path('supprimer-tache/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
    path('ajouter-liste/', views.ajouter_liste, name='ajouter_liste'),
    path('supprimer-liste/<int:liste_id>/', views.supprimer_liste, name='supprimer_liste'),
    path('modifier_liste/<int:liste_id>/', views.modifier_liste, name='modifier_liste'),

]
