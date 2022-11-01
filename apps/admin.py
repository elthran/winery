from django.contrib import admin

# Register your models here.
from apps.models.choices import VintageChoices, VarietalChoices, VineyardChoices, GrowerChoices, BlockChoices, \
    UnitChoices, VesselChoices, CrushOrderTypeChoices
from apps.models.models import FruitIntake, Docket

try:
    for i in range(2012,2022):
        p = VintageChoices(choice=i)
        p.save()
    p = VarietalChoices(choice="Pinot Noir")
    p.save()
    p = VineyardChoices(choice="Blue Grouse")
    p.save()
    p = GrowerChoices(choice="Jacob")
    p.save()
    p = BlockChoices(choice=13)
    p.save()
    p = UnitChoices(choice="kg")
    p.save()
    p = VesselChoices(choice="TANK 01")
    p.save()
    p = CrushOrderTypeChoices(choice="Crush & Press")
    p.save()
    p = CrushOrderTypeChoices(choice="Crush Only")
    p.save()
    p = CrushOrderTypeChoices(choice="Whole Cluster Press")
    p.save()

    docket = Docket(docket_number="2012BlueGrousePinotNoir13", vintage=2012, grower="Jacob", varietal="Pinot Noir", vineyard="Blue Grouse", block=13)
    docket.save()
    docket2 = Docket(docket_number="2011BlueGrousePinotNoir13", vintage=2011, grower="Jacob", varietal="Pinot Noir", vineyard="Blue Grouse", block=13)
    docket2.save()

    fruit_intake = FruitIntake(number_of_bins=5, total_weight=2, tare_weight=1, units="kg")
    fruit_intake.save()
    fruit_intake.docket = docket
    fruit_intake.save()

    fruit_intake = FruitIntake(number_of_bins=5, total_weight=7, tare_weight=3, units="kg")
    fruit_intake.save()
    fruit_intake.docket = docket2
    fruit_intake.save()
except:
    pass