from django.contrib import admin
from .models import Compte
# Register your models here.
@admin.register(Compte)
class Compte(admin.ModelAdmin):
    #definition des colonnes dans liste
    list_display =('username', 'email', 'date_joined')
    
    #pour effectuer une recherche
    search_fields = ('username', 'email', 'date_joined')