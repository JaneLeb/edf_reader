from django.db import models
from common.models import UUIDModel, TimeStampedModel
from apps.patients.models import Patient

class HolterRecord(UUIDModel, TimeStampedModel):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Загружен"
        PARSING = "parsing", "Парсинг"
        READY = "ready", "Готов"
        ERROR = "error", "Ошибка"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                related_name="holter_records", null=True, blank=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    duration_hours = models.PositiveIntegerField(default=0)
    sampling_rate = models.PositiveIntegerField(default=0)
    channels = models.JSONField(default=list, blank=True)
    edf_file = models.FileField(upload_to="edf/%Y/%m/")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"Holter {self.id} ({self.status})"

class HolterEvent(UUIDModel, TimeStampedModel):
    class EventType(models.TextChoices):
        SYMPTOM = "symptom", "Симптом"
        ACTIVITY = "activity", "Активность"
        MEDICATION = "medication", "Лекарство"
        OTHER = "other", "Другое"

    record = models.ForeignKey(HolterRecord, on_delete=models.CASCADE, related_name="events")
    time_offset_sec = models.FloatField()
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    text = models.TextField(blank=True)
    severity = models.PositiveSmallIntegerField(null=True, blank=True)