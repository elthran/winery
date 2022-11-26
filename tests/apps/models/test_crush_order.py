from django.test import TestCase

from apps.models.crush_orders import CrushOrder


class CrushOrderTestCase(TestCase):
    def setUp(self):
        CrushOrder.objects.create(
            vintage=2022, crush_type="Whole Cluster Press", date="2022-09-30"
        )

    def test_total_weight(self):
        """Total weight calculation is correct."""
        crash_order = CrushOrder.objects.get(date="2022-09-30")

        self.assertEqual(crash_order.total_weight, 77)
