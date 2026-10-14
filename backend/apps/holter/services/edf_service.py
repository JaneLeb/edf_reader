import ecg_native
from pathlib import Path

def probe_edf(path: str) -> dict:
    hdr = ecg_native.read_header(path)
    return {
        "signals": hdr.signals,
        "duration_sec": hdr.duration_sec,
        "labels": list(hdr.labels),
        "sample_rates": list(hdr.sample_rates),
        "samples_per_signal": list(hdr.samples_per_signal),
    }

def load_channel(path: str, channel: int = 0):
    return ecg_native.read_signal(path, channel)