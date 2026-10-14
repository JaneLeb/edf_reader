from django.db import models
from common.models import UUIDModel, TimeStampedModel
from apps.holter.models import HolterRecord

class AnalysisResult(UUIDModel, TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидание"
        RUNNING = "running", "Выполняется"
        DONE = "done", "Готово"
        FAILED = "failed", "Ошибка"

    holter_record = models.OneToOneField(HolterRecord, on_delete=models.CASCADE,
                                         related_name="analysis")
    model_version = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    finished_at = models.DateTimeField(null=True, blank=True)

class AnomalySegment(UUIDModel):
    analysis = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE, related_name="segments")
    start_sec = models.FloatField()
    end_sec = models.FloatField()
    risk_start = models.FloatField()
    risk_end = models.FloatField()
    risk_min = models.FloatField()
    risk_max = models.FloatField()
    label = models.CharField(max_length=50, blank=True)
    confidence = models.FloatField(default=0.0)