from django.core.management.base import BaseCommand
from django.db import transaction

from checker.models import BgmiVersion, Brand, Device
from checker.seed import BRANDS, DEVICES, VERSIONS


class Command(BaseCommand):
    help = "Load brands, phones and BGMI versions from the project PDFs (safe to run again)."

    @transaction.atomic
    def handle(self, *args, **options):
        brands = {name: Brand.objects.get_or_create(brand_name=name)[0] for name in BRANDS}

        for brand, segment, name, chipset, score in DEVICES:
            Device.objects.update_or_create(
                brand=brands[brand], device_name=name,
                defaults={"segment": segment, "chipset": chipset, "antutu_score": score},
            )

        for version, min_score, fps in VERSIONS:
            # download_url is only set on creation, so links added in the admin panel are kept.
            BgmiVersion.objects.update_or_create(
                version_name=version,
                defaults={"min_antutu_score": min_score, "target_fps": fps},
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Brand.objects.count()} brands, {Device.objects.count()} devices, "
            f"{BgmiVersion.objects.count()} BGMI versions."))
