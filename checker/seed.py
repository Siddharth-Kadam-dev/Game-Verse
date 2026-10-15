"""Seed data taken from Smartphone_table.pdf and BGMI_Versions.pdf."""

BRANDS = ["Samsung", "Xiaomi / Redmi", "Realme", "Vivo", "Apple"]

# (brand, segment, device_name, chipset, AnTuTu v10 score)
DEVICES = [
    ("Samsung", "Entry", "Galaxy A05", "MediaTek Helio G85", 215000),
    ("Samsung", "Budget", "Galaxy M15 5G", "MediaTek Dimensity 6100+", 410000),
    ("Samsung", "Mid-Range", "Galaxy A35 5G", "Exynos 1380", 600000),
    ("Samsung", "Upper Mid", "Galaxy S23 FE", "Exynos 2200", 1180000),
    ("Samsung", "Flagship", "Galaxy S24 Ultra", "Snapdragon 8 Gen 3", 1810000),
    ("Xiaomi / Redmi", "Entry", "Redmi A3", "MediaTek Helio G36", 127000),
    ("Xiaomi / Redmi", "Budget", "Redmi Note 13 5G", "MediaTek Dimensity 6080", 455000),
    ("Xiaomi / Redmi", "Mid-Range", "Redmi Note 13 Pro+ Ultra", "MediaTek Dimensity 7200 Ultra", 720000),
    ("Xiaomi / Redmi", "Upper Mid", "Xiaomi 14 Civi", "Snapdragon 8s Gen 3", 1450000),
    ("Xiaomi / Redmi", "Flagship", "Xiaomi 14 Ultra", "Snapdragon 8 Gen 3", 2014000),
    ("Realme", "Entry", "Realme C51", "Unisoc T612", 250000),
    ("Realme", "Budget", "Realme 12x 5G", "MediaTek Dimensity 6100+", 415000),
    ("Realme", "Mid-Range", "Realme 12 Pro+ 5G", "Snapdragon 7s Gen 2", 660000),
    ("Realme", "Upper Mid", "Realme GT 6T", "Snapdragon 7+ Gen 3", 1500000),
    ("Realme", "Flagship", "Realme GT 6", "Snapdragon 8s Gen 3", 1560000),
    ("Vivo", "Entry", "Vivo Y18i", "Unisoc T612", 245000),
    ("Vivo", "Budget", "Vivo T3x 5G", "Snapdragon 6 Gen 1", 560000),
    ("Vivo", "Mid-Range", "Vivo T3 Pro 5G", "Snapdragon 7 Gen 3", 820000),
    ("Vivo", "Upper Mid", "Vivo V40 Pro", "MediaTek Dimensity 9200+", 1520000),
    ("Vivo", "Flagship", "Vivo X100 Pro", "MediaTek Dimensity 9300", 2100000),
    ("Apple", "Entry-Premium", "iPhone SE (3rd Gen)", "A15 Bionic", 1250000),
    ("Apple", "Mid-Premium", "iPhone 13", "A15 Bionic (5-core GPU)", 1310000),
    ("Apple", "Upper Premium", "iPhone 14", "A15 Bionic", 1330000),
    ("Apple", "Flagship", "iPhone 15", "A16 Bionic", 1470000),
    ("Apple", "Ultra Flagship", "iPhone 15 Pro Max", "A17 Pro", 1640000),
]

# (version_name, min AnTuTu v10 score, target FPS)
VERSIONS = [
    ("3.0", 300000, "40 - 60 FPS"),
    ("3.1", 350000, "40 - 60 FPS"),
    ("3.2", 400000, "60 FPS"),
    ("3.3", 450000, "60 FPS"),
    ("3.4", 550000, "60 FPS"),
    ("3.5", 700000, "60 - 90 FPS"),
    ("3.6", 850000, "90 FPS"),
    ("4.0", 1000000, "90 FPS"),
    ("4.5", 1400000, "90 - 120 FPS"),
    ("4.6", 1800000, "Locked 120 FPS"),
]
