from django.db import models
from patients.models import Patient

class Paiement(models.Model):
    MODE_CHOICES = [
        ('especes', 'Espèces'),
        ('mobile_money', 'Mobile Money (Airtel/MTN)'),
        ('carte', 'Carte Bancaire'),
    ]
    
    STATUT_CHOICES = [
        ('paye', 'Payé'),
        ('en_attente', 'En attente'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='paiements', null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES, default='especes')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='paye')
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date']

    def __str__(self):
        return f"Facture #{self.id} - {self.montant} FCFA ({self.patient})"
