from django.contrib import admin
from django.urls import path, include

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
