from django.urls import path

from . import views

app_name = 'checker'

urlpatterns = [
    path("", views.index, name="index"),
    path("api/brands", views.api_brands, name="api-brands"),
    path("api/devices", views.api_devices, name="api-devices"),
    path("api/versions", views.api_versions, name="api-versions"),
    path("api/check/device/<int:device_id>", views.api_check_device, name="api-check-device"),
    path("api/check/score", views.api_check_score, name="api-check-score"),
]