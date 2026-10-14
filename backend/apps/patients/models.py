from django.db import models
from common.models import UUIDModel, TimeStampedModel

class Patient(UUIDModel, TimeStampedModel):
    class Sex(models.TextChoices):
        M = "M", "Мужской"
        F = "F", "Женский"

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True)
    medical_card_no = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.medical_card_no})"