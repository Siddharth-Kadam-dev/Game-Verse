from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import BgmiVersion, CompatibilityCheck, Device
from .seed import DEVICES, VERSIONS


class CheckerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_data", verbosity=0)

    def get_json(self, name, *args, **params):
        response = self.client.get(reverse(name, args=args), params)
        return response, response.json()

    def test_seed_counts(self):
        self.assertEqual(BgmiVersion.objects.count(), len(VERSIONS))
        self.assertEqual(Device.objects.count(), len(DEVICES))

    def test_score_picks_newest_supported_version(self):
        _, data = self.get_json("api-check-score", antutu="650,000")
        self.assertEqual(data["recommended"]["version"], "3.4")
        self.assertEqual(data["next_upgrade"]["version"], "3.5")
        self.assertEqual(data["next_upgrade"]["gap"], 50000)

    def test_exact_minimum_counts_as_supported(self):
        _, data = self.get_json("api-check-score", antutu="1800000")
        self.assertEqual(data["recommended"]["version"], "4.6")
        self.assertIsNone(data["next_upgrade"])

    def test_score_below_lowest_requirement(self):
        _, data = self.get_json("api-check-score", antutu="215000")
        self.assertIsNone(data["recommended"])
        self.assertEqual(data["next_upgrade"]["version"], "3.0")
        self.assertEqual(data["next_upgrade"]["gap"], 85000)
        self.assertFalse(any(v["supported"] for v in data["versions"]))

    def test_device_mode(self):
        device = Device.objects.get(device_name="Galaxy S24 Ultra")
        _, data = self.get_json("api-check-device", device.device_id)
        self.assertEqual(data["recommended"]["version"], "4.6")
        self.assertEqual(data["device"]["brand"], "Samsung")

    def test_every_device_matches_the_rule(self):
        for device in Device.objects.all():
            _, data = self.get_json("api-check-device", device.device_id)
            expected = [v for v, m, _ in VERSIONS if m <= device.antutu_score]
            self.assertEqual(data["recommended"]["version"] if data["recommended"] else None,
                             expected[-1] if expected else None, device.device_name)

    def test_bad_input_is_rejected(self):
        for value in ["abc", "0", "-5", "99999999999", ""]:
            response, data = self.get_json("api-check-score", antutu=value)
            self.assertEqual(response.status_code, 400, value)
            self.assertIn("error", data)
        response, _ = self.get_json("api-check-device", 99999)
        self.assertEqual(response.status_code, 404)

    def test_checks_are_logged(self):
        self.get_json("api-check-score", antutu="650000")
        device = Device.objects.get(device_name="Redmi A3")
        self.get_json("api-check-device", device.device_id)
        self.assertEqual(CompatibilityCheck.objects.count(), 2)
        self.assertIsNone(CompatibilityCheck.objects.get(device=device).version)

    def test_dropdown_endpoints_and_page(self):
        _, brands = self.get_json("api-brands")
        self.assertEqual([b["name"] for b in brands][:2], ["Samsung", "Xiaomi / Redmi"])
        _, devices = self.get_json("api-devices", brand_id=brands[0]["brand_id"])
        self.assertEqual(len(devices), 5)
        page = self.client.get(reverse("index"))
        self.assertContains(page, "BGMI Compatibility Checker")
        self.assertContains(page, "checker/app.js")
