from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import get_user_model

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



User = get_user_model()
try:
    if not User.objects.filter(username="admin_bernadette").exists():
        User.objects.create_superuser(
            username="Bernadette", 
            email="donimatsiona@gmail.com", 
            password="Berna@1234" # Pensez à le changer après votre première connexion
        )
        print("🎉 Superuser créé avec succès dans PostgreSQL !")
except Exception:
    pass
