from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from medecins.models import Medecin  # Assurez-vous que cette app possède un modèle Medecin

class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de validation'),
        ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
    ]

    MOTIF_CHOICES = [
        ('consultation_generale', 'Consultation ORL Générale'),
        ('audiometrie', 'Bilan Auditif / Audiométrie'),
        ('sinusite', 'Troubles des Sinus / Nez bouché'),
        ('pharyngite', 'Maux de Gorge / Cordes Vocales'),
        ('vertiges', 'Gestion des Vertiges / Équilibre'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendezvous')
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='rendezvous')
    date_rdv = models.DateField(null=False, blank=False)
    heure_rdv = models.TimeField(null=False, blank=False)
    motif = models.CharField(max_length=50, choices=MOTIF_CHOICES)
    notes = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['date_rdv', 'heure_rdv']

    def __str__(self):
        return f"RDV #{self.id} - {self.patient} le {self.date_rdv}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    rdv = models.ForeignKey(RendezVous, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient}: {self.message[:50]}"
