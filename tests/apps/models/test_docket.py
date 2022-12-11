from django.test import TestCase

from apps.models import Docket, FruitIntake


class DocketTestCase(TestCase):
    def setUp(self):
        docket = Docket.objects.create(
            docket_number="2022 BG PN CJ A1",
            grower="Blue Grouse",
            varietal="Pinot Noir",
            vineyard="Charles & Jacob",
            vintage=2022,
            block="A1",
        )
        fruit_intake1 = FruitIntake.objects.create(
            docket=docket,
            number_of_bins=1,
            total_weight=182.00,
            tare_weight=42.00,
            units="kg",
            date="2021-10-10",
        )
        fruit_intake2 = FruitIntake.objects.create(
            docket=docket,
            number_of_bins=1,
            total_weight=193.00,
            tare_weight=37.00,
            units="kg",
            date="2021-10-10",
        )

    def test_fruit_weight(self):
        """Fruit weight calculation is correct."""
        docket = Docket.objects.get(
            docket_number="2022 Blue Grouse Pinot Noir Charles & Jacob A1"
        )

        self.assertEqual(docket.fruit_weight, 296)
