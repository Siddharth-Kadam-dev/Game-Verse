import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameverse.settings')
django.setup()

from checker.models import (
    ApkScan, Brand, CompatibilityCheck, Device, 
    DownloadHistory, Game, UserDevice, VersionFeedback
)

# Clear dependent models first to satisfy PROTECT foreign key constraints
ApkScan.objects.all().delete()
DownloadHistory.objects.all().delete()
VersionFeedback.objects.all().delete()
CompatibilityCheck.objects.all().delete()
UserDevice.objects.all().delete()

# Clear parent models
Device.objects.all().delete()
Brand.objects.all().delete()
Game.objects.all().delete()

# Seed Brands
brands = ["Samsung", "Xiaomi / Redmi", "Realme", "Vivo", "Apple"]
brand_objs = {b: Brand.objects.create(brand_name=b) for b in brands}

# Seed Devices
devices_data = [
    ("Samsung", "Galaxy A05", "Entry", "MediaTek Helio G85", 215000),
    ("Samsung", "Galaxy M15 5G", "Budget", "MediaTek Dimensity 6100+", 410000),
    ("Samsung", "Galaxy A35 5G", "Mid-Range", "Exynos 1380", 600000),
    ("Samsung", "Galaxy S23 FE", "Upper Mid", "Exynos 2200", 1180000),
    ("Samsung", "Galaxy S24 Ultra", "Flagship", "Snapdragon 8 Gen 3", 1810000),
    ("Xiaomi / Redmi", "Redmi A3", "Entry", "MediaTek Helio G36", 127000),
    ("Xiaomi / Redmi", "Redmi Note 13 5G", "Budget", "MediaTek Dimensity 6080", 455000),
    ("Xiaomi / Redmi", "Xiaomi 14 Ultra", "Flagship", "Snapdragon 8 Gen 3", 2014000),
    ("Realme", "Realme C51", "Entry", "Unisoc T612", 250000),
    ("Realme", "Realme GT 6", "Flagship", "Snapdragon 8s Gen 3", 1560000),
    ("Vivo", "Vivo T3x 5G", "Budget", "Snapdragon 6 Gen 1", 560000),
    ("Vivo", "Vivo X100 Pro", "Flagship", "MediaTek Dimensity 9300", 2100000),
    ("Apple", "iPhone 13", "Mid-Premium", "A15 Bionic", 1310000),
    ("Apple", "iPhone 15 Pro Max", "Ultra Flagship", "A17 Pro", 1640000),
]

for b_name, d_name, seg, chip, score in devices_data:
    Device.objects.create(
        brand=brand_objs[b_name],
        device_name=d_name,
        segment=seg,
        chipset=chip,
        antutu_score=score
    )

# Seed Games
games_data = [
    ("BGMI (India)", "3.6", 450000, "60 - 90 FPS"),
    ("PUBG Mobile (Global)", "3.6", 450000, "60 - 90 FPS"),
    ("PUBG Mobile Lite", "0.28.0", 200000, "40 - 60 FPS"),
    ("PUBG Mobile (KR / Korea)", "3.6", 450000, "60 - 90 FPS"),
    ("Game for Peace (China)", "1.29", 500000, "60 - 90 FPS"),
    ("Free Fire MAX", "1.108", 250000, "60 FPS"),
    ("Call of Duty: Mobile", "1.0.48", 400000, "60 - 90 FPS"),
    ("Call of Duty: Warzone Mobile", "3.10", 850000, "60 - 120 FPS"),
    ("Minecraft", "1.21", 180000, "60 FPS"),
]

for g_name, ver, min_score, fps in games_data:
    Game.objects.create(
        name=g_name,
        current_version=ver,
        min_antutu_score=min_score,
        target_fps=fps
    )

print(f"SUCCESS: Created {Brand.objects.count()} Brands, {Device.objects.count()} Devices, and {Game.objects.count()} Games!")