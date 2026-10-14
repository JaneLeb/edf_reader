from rest_framework import serializers
from .models import HolterRecord, HolterEvent

class HolterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolterEvent
        fields = ["id", "time_offset_sec", "event_type", "text", "severity"]

class HolterRecordSerializer(serializers.ModelSerializer):
    events = HolterEventSerializer(many=True, read_only=True)

    class Meta:
        model = HolterRecord
        fields = ["id", "patient", "start_datetime", "duration_hours",
                  "sampling_rate", "channels", "edf_file", "status",
                  "error_message", "events", "created_at"]
        read_only_fields = ["status", "duration_hours", "sampling_rate",
                            "channels", "error_message"]