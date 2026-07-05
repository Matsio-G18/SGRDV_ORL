from django.contrib import admin
from .models import Medecin

# Register your models here.
@admin.register(Medecin)
class Medecin(admin.ModelAdmin):
    #pour afficher une colonne dans notre interface admin
    list_display = ('nom', 'specialite', 'telephone')
    search_fields = ('nom', 'specialite')