from django.contrib import admin

# Register your models here.
from dockets.models.choices import VintageChoices, VarietalChoices, VineyardChoices, GrowerChoices, BlockChoices, \
    UnitChoices

try:
    p = VintageChoices(choice=2012)
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
except:
    pass