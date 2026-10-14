import os
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import HolterRecord
from .serializers import HolterRecordSerializer
from .services.edf_service import probe_edf, load_channel

class HolterRecordViewSet(viewsets.ModelViewSet):
    queryset = HolterRecord.objects.all().order_by("-created_at")
    serializer_class = HolterRecordSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        record = serializer.save(status=HolterRecord.Status.PARSING)
        try:
            meta = probe_edf(record.edf_file.path)
            record.duration_hours = int(meta["duration_sec"] // 3600)
            record.sampling_rate = int(meta["sample_rates"][0]) if meta["sample_rates"] else 0
            record.channels = meta["labels"]
            record.status = HolterRecord.Status.READY
        except Exception as e:
            record.status = HolterRecord.Status.ERROR
            record.error_message = str(e)
        record.save()

    @action(detail=True, methods=["get"], url_path="signal")
    def signal(self, request, pk=None):
        record = self.get_object()
        channel = int(request.query_params.get("channel", 0))
        try:
            data = load_channel(record.edf_file.path, channel)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        fs = record.sampling_rate or 1
        # Прореживание: не более 100 000 точек на ответ
        step = max(1, len(data) // 100_000)
        values = data[::step].tolist()
        times = [i * step / fs for i in range(len(values))]
        return Response({
            "fs": fs,
            "channel": channel,
            "step": step,
            "times": times,
            "values": values,
        })