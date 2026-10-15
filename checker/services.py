"""Compatibility rules: newest BGMI version whose minimum AnTuTu score the phone meets."""
from django.db.models import BooleanField, Case, Value, When

from .models import BgmiVersion, CompatibilityCheck


def serialize_version(v, supported=None):
    return {
        "version_id": v.version_id,
        "version": v.version_name,
        "min_antutu": v.min_antutu_score,
        "fps_label": v.target_fps,
        "download_url": v.download_url,
        "supported": supported,
    }


def serialize_device(d):
    return {
        "device_id": d.device_id,
        "brand_id": d.brand_id,
        "brand": d.brand.brand_name,
        "model": d.device_name,
        "segment": d.segment,
        "chipset": d.chipset,
        "antutu_score": d.antutu_score,
    }


def evaluate(score, mode, device=None, user=None):
    """Compare a score with every BGMI version (in the database), log it, return the result."""
    versions = list(
        BgmiVersion.objects.annotate(
            supported=Case(
                When(min_antutu_score__lte=score, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by("min_antutu_score")
    )
    ok = [v for v in versions if v.supported]
    locked = [v for v in versions if not v.supported]
    best = ok[-1] if ok else None

    next_upgrade = None
    if locked:
        next_upgrade = serialize_version(locked[0], False)
        next_upgrade["gap"] = locked[0].min_antutu_score - score

    CompatibilityCheck.objects.create(
        user=user if (user is not None and user.is_authenticated) else None,
        mode=mode,
        device=device,
        antutu_score=score,
        version=best,
    )
    return {
        "mode": mode,
        "antutu": score,
        "device": serialize_device(device) if device else None,
        "recommended": serialize_version(best, True) if best else None,
        "next_upgrade": next_upgrade,
        "versions": [serialize_version(v, v.supported) for v in versions],
    }
