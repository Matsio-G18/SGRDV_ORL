from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import get_user_model
from django.db import connection

urlpatterns = [
    path('', __import__('SGRDV_ORL.views').views.home, name='home'),
    path('admin/', admin.site.urls),
    path('comptes/', include('comptes.urls')),
    path('medecins/', include('medecins.urls')),
    path('patients/', include('patients.urls')),
    path('rdv/', include('rdv.urls')),
    path('paiements/', include('paiements.urls')),
]


# Personnalisation des textes de l'administration Django
admin.site.site_header = "BERNADETTE — Administration ORL"
admin.site.site_title = "Panel Admin BERNADETTE"
admin.site.index_title = "Systeme de gestion de rendez-vous"



# =====================================================================
# SCRIPT DE CRÉATION DE L'ADMINISTRATEUR DANS POSTGRESQL (RENDER FREE)
# =====================================================================


User = get_user_model()

#accès pour l'interface Jazzmin
ADMIN_USER = "Bernadette"
ADMIN_PASS = "Berna@1234" # Utilisez un mot de passe robuste
ADMIN_MAIL = "donimatsiona@gmail.com"

try:
    # On vérifie si la table des utilisateurs existe déjà pour éviter de planter
    if "auth_user" in connection.introspection.table_names():
        if not User.objects.filter(username=ADMIN_USER).exists():
            User.objects.create_superuser(
                username=ADMIN_USER, 
                email=ADMIN_MAIL, 
                password=ADMIN_PASS
            )
            print(f"🎉 Le compte Administrateur '{ADMIN_USER}' a été injecté dans PostgreSQL !")
        else:
            print(f"ℹ️ Le compte '{ADMIN_USER}' est déjà présent dans PostgreSQL.")
except Exception as e:
    print(f"Erreur d'injection de l'administrateur : {e}")

