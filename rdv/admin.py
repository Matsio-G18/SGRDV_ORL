from django.contrib import admin
from .models import Notification, RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'medecin', 'date_rdv', 'heure_rdv', 'motif', 'statut')
    list_filter = ('statut', 'date_rdv', 'medecin')
    search_fields = ('patient__nom', 'patient__prenom', 'motif')
    list_editable = ('statut',)  # Permet de changer le statut directement depuis la liste
    date_hierarchy = 'date_rdv'  # Barre chronologique en haut du panneau


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
