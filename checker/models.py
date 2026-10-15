"""Database tables for GameVerse.

Core tables:       User, Device, Game
Additional tables: Brand, UserDevice, CompatibilityCheck, DownloadHistory,
                   VersionFeedback, ApkScan
"""
import django
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


def _check(condition, name):
    """CheckConstraint helper: Django 5.1 renamed `check=` to `condition=`."""
    key = "condition" if django.VERSION >= (5, 1) else "check"
    return models.CheckConstraint(name=name, **{key: condition})


class User(AbstractUser):
    """Table `users`: Django's login user plus a role (user or admin)."""

    ROLE_CHOICES = [("user", "User"), ("admin", "Admin")]

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    class Meta:
        db_table = "users"

    @property
    def name(self):
        return self.get_full_name() or self.username


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "brands"
        ordering = ["brand_id"]

    def __str__(self):
        return self.brand_name


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="devices")
    device_name = models.CharField(max_length=100)
    segment = models.CharField(max_length=30)
    chipset = models.CharField(max_length=80)
    antutu_score = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="AnTuTu v10 score")
    min_ram_gb = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1)],
                                                  help_text="Lowest RAM variant of the model, in GB")
    android_version = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Empty for iPhone")
    storage_gb = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "devices"
        ordering = ["antutu_score"]
        constraints = [
            models.UniqueConstraint(fields=["brand", "device_name"], name="uq_device_brand_name"),
            _check(Q(antutu_score__gt=0), "ck_device_antutu_positive"),
        ]
        indexes = [models.Index(fields=["antutu_score"], name="idx_devices_antutu")]

    def __str__(self):
        return f"{self.brand.brand_name} {self.device_name}"


class Game(models.Model):
    """Supports multiple games, each tracking only its latest active version."""

    game_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, help_text="Game Name (e.g., BGMI, PUBG Mobile Lite)")
    current_version = models.CharField(max_length=30, help_text="Latest running version e.g. 3.6")
    min_antutu_score = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                                   help_text="Minimum AnTuTu v10 score needed")
    target_fps = models.CharField(max_length=30, default="60 FPS", help_text="e.g. 60 - 90 FPS")
    min_ram_gb = models.PositiveSmallIntegerField(null=True, blank=True)
    min_android_version = models.PositiveSmallIntegerField(null=True, blank=True)
    download_url = models.TextField(default="#", help_text="Blank placeholder '#' until a real link is added")

    class Meta:
        db_table = "games"
        ordering = ["name"]
        constraints = [_check(Q(min_antutu_score__gt=0), "ck_game_antutu_positive")]
        indexes = [models.Index(fields=["min_antutu_score"], name="idx_games_min_score")]

    def __str__(self):
        return f"{self.name} (v{self.current_version})"


class UserDevice(models.Model):
    """Saved device profiles (users and devices, many to many)."""

    user_device_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_devices")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="saved_by")
    nickname = models.CharField(max_length=50, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_devices"
        constraints = [models.UniqueConstraint(fields=["user", "device"], name="uq_user_device")]


class CompatibilityCheck(models.Model):
    """History of every check in both modes. Guests are allowed (user is empty)."""

    MODE_CHOICES = [("device", "Pick your phone"), ("score", "Enter AnTuTu score")]

    check_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="checks")
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.PROTECT, related_name="checks")
    antutu_score = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="checks", help_text="Tested Game")
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "compatibility_checks"
        ordering = ["-checked_at"]
        constraints = [
            _check(
                (Q(mode="device") & Q(device__isnull=False)) | (Q(mode="score") & Q(device__isnull=True)),
                "ck_check_mode_device",
            ),
        ]
        indexes = [models.Index(fields=["user"], name="idx_checks_user")]


class DownloadHistory(models.Model):
    download_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="downloads")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="downloads")
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "download_history"
        ordering = ["-downloaded_at"]
        verbose_name_plural = "download history"


class VersionFeedback(models.Model):
    """Community lag / FPS reports, one per user, game and phone."""

    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedback")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="feedback")
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="feedback")
    avg_fps = models.PositiveSmallIntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(1), MaxValueValidator(120)])
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "version_feedback"
        verbose_name_plural = "version feedback"
        constraints = [
            models.UniqueConstraint(fields=["user", "game", "device"], name="uq_feedback_user_game_device"),
            _check(Q(rating__gte=1) & Q(rating__lte=5), "ck_feedback_rating"),
        ]
        indexes = [models.Index(fields=["game"], name="idx_feedback_game")]


class ApkScan(models.Model):
    """Safety scan result for each game's file."""

    STATUS_CHOICES = [("pending", "Pending"), ("clean", "Clean"), ("flagged", "Flagged")]

    scan_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="scans")
    scan_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    scanner_note = models.TextField(blank=True)
    scanned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "apk_scans"