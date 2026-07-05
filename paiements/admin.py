from django.contrib import admin
from .models import Paiement
# Register your models here.
@admin.register(Paiement)
class Paiement(admin.ModelAdmin):
    #liste des colonnes pour afficher sur l'interface admin
    list_display = ('montant', 'description', 'date')