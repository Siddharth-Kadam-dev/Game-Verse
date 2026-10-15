from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import (
    ApkScan, Brand, CompatibilityCheck, Device, DownloadHistory,
    Game, User, UserDevice, VersionFeedback
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    fieldsets = DjangoUserAdmin.fieldsets + (("GameVerse", {"fields": ("role",)}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("GameVerse", {"fields": ("email", "role")}),)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("brand_name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_name", "brand", "segment", "chipset", "antutu_score", "min_ram_gb")
    list_filter = ("brand", "segment")
    search_fields = ("device_name", "chipset")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Admin panel: Manage games, current versions, and download links."""
    list_display = ("name", "current_version", "min_antutu_score", "target_fps", "download_url")
    list_editable = ("download_url", "current_version")
    search_fields = ("name",)


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "device", "nickname", "added_at")


@admin.register(CompatibilityCheck)
class CompatibilityCheckAdmin(admin.ModelAdmin):
    list_display = ("checked_at", "mode", "device", "antutu_score", "game", "user")
    list_filter = ("mode", "game")


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ("downloaded_at", "user", "game")


@admin.register(VersionFeedback)
class VersionFeedbackAdmin(admin.ModelAdmin):
    list_display = ("game", "device", "user", "rating", "avg_fps", "created_at")
    list_filter = ("game", "rating")


@admin.register(ApkScan)
class ApkScanAdmin(admin.ModelAdmin):
    list_display = ("game", "scan_status", "scanned_at")
    list_filter = ("scan_status",)