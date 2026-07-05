from django.contrib import admin
from .models import Patient  # Assurez-vous d'avoir créé le modèle Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste globale
    list_display = ('user', 'telephone', 'date_naissance', 'groupe_sanguin')
    
    # Barre de recherche rapide
    search_fields = ('user__username', 'user__last_name', 'telephone')
    
    # Filtres latéraux pratiques
    list_filter = ('groupe_sanguin',)
