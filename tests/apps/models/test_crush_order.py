from django.test import TestCase

from apps.models.crush_orders import CrushOrder
from apps.models import CrushOrderDocketMapping
from apps.models.dockets import Docket


class CrushOrderTestCase(TestCase):
    def setUp(self):
        crush_order = CrushOrder.objects.create(
            vintage=2022, crush_type="Whole Cluster Press", date="2022-09-30"
        )
        docket1 = Docket.objects.create(
            grower="Blue Grouse",
            varietal="Pinot Noir",
            vineyard="Charles & Jacob",
            vintage=2022,
            block="A1",
        )
        docket2 = Docket.objects.create(
            grower="Blue Grouse",
            varietal="Chardonnay",
            vineyard="Charles & Jacob",
            vintage=2022,
            block="B3",
        )
        docket3 = Docket.objects.create(
            grower="Blue Grouse",
            varietal="Pinot Noir",
            vineyard="Paula",
            vintage=2022,
            block="A5",
        )
        CrushOrderDocketMapping.objects.create(
            crush_order=crush_order,
            docket=docket1,
            quantity=140,
            units="kg",
        )
        CrushOrderDocketMapping.objects.create(
            crush_order=crush_order,
            docket=docket2,
            quantity=351,
            units="kg",
        )
        CrushOrderDocketMapping.objects.create(
            crush_order=crush_order,
            docket=docket3,
            quantity=233,
            units="kg",
        )

    def test_total_weight(self):
        """Total weight calculation is correct."""
        crash_order = CrushOrder.objects.get(date="2022-09-30")

        self.assertEqual(crash_order.total_weight, 724)
