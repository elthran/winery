from annoying.functions import get_object_or_None
from django.contrib import admin
import django

# Register your models here.

from apps.models.choices import VintageChoices, VarietalChoices, VineyardChoices, GrowerChoices, BlockChoices, \
    UnitChoices, CrushOrderTypeChoices, VesselIdChoices, VesselTypeChoices
from apps.models.crush_orders import CrushOrder
from apps.models.dockets import Docket
from apps.models.fruit_intakes import FruitIntake
from apps.models.models import CrushOrderDocketMapping, CrushOrderVesselMapping
from apps.models.vessels import Vessel

growers = ["Blue Grouse", "Green Gage Farm"]
vintages = [2022]
varietals = ["Pinot Noir", "Chardonnay", "Schönburger", "Siegerrebe", "Ortega"]
vineyards = ["Charles & Jacob", "Paula", "Unknown"]
blocks = [f"{letter}{number}" for number in range(1, 6) for letter in ["A", "B", "C"]]
units = ["kg"]
crush_types = ["Crush & Press", "Crush Only", "Whole Cluster Press"]
vessels = [
    {"type_name": "tank", "type_id": "1", "expansion_chamber_diameter": 0.0001, "expansion_chamber_height": 0.0001,
     "expansion_chamber_radius": 0.00005, "tank_diameter": 183, "top_cone_height": 0.0001, "cylinder_height": 198,
     "cylinder_radius": 91.5, "floor_height": 16},
    {"type_name": "tank", "type_id": "2", "expansion_chamber_diameter": 0.0001, "expansion_chamber_height": 0.0001,
     "expansion_chamber_radius": 0.00005, "tank_diameter": 118, "top_cone_height": 10, "cylinder_height": 170,
     "cylinder_radius": 59, "floor_height": 10},
    {"type_name": "tank", "type_id": "3", "expansion_chamber_diameter": 0.0001, "expansion_chamber_height": 0.0001,
     "expansion_chamber_radius": 0.00005, "tank_diameter": 79, "top_cone_height": 10, "cylinder_height": 93,
     "cylinder_radius": 39.5, "floor_height": 10},
    {"type_name": "tank", "type_id": "4", "expansion_chamber_diameter": 0.0001, "expansion_chamber_height": 0.0001,
     "expansion_chamber_radius": 0.00005, "tank_diameter": 97, "top_cone_height": 0.0001, "cylinder_height": 147,
     "cylinder_radius": 48.5, "floor_height": 10},
]

dockets = [
    {"number": "2022 BG PN CJ A1", "grower": "Blue Grouse", "varietal": "Pinot Noir", "vineyard": "Charles & Jacob", "vintage": 2022, "block": "A1"},
    {"number": "2022 BG CD CJ B3", "grower": "Blue Grouse", "varietal": "Chardonnay", "vineyard": "Charles & Jacob", "vintage": 2022, "block": "B3"},
    {"number": "2022 BG PN PA A5", "grower": "Blue Grouse", "varietal": "Pinot Noir", "vineyard": "Paula", "vintage": 2022, "block": "A5"},
    {"number": "2022 GG SB BN B5", "grower": "Green Gage Farm", "varietal": "Schönburger", "vineyard": "Brunner", "vintage": 2022, "block": "B5"},
    {"number": "2022 BG SG PA C2", "grower": "Blue Grouse", "varietal": "Siegerrebe", "vineyard": "Paula", "vintage": 2022, "block": "C2"},
]
fruit_intakes = [
    {"docket": "2022 Blue Grouse Pinot Noir Charles & Jacob A1", "bins": 1, "total_weight": 182.00, "tare_weight": 42.00, "units": "kg"},
    {"docket": "2022 Blue Grouse Chardonnay Charles & Jacob B3", "bins": 1, "total_weight": 393.00, "tare_weight": 42.00, "units": "kg"},
    {"docket": "2022 Blue Grouse Pinot Noir Paula A5", "bins": 26, "total_weight": 257.50, "tare_weight": 24.50, "units": "kg"},
    {"docket": "2022 Green Gage Farm Schönburger Brunner B5", "bins": 12, "total_weight": 5443.50, "tare_weight": 660.00, "units": "kg"},
    {"docket": "2022 Blue Grouse Siegerrebe Paula C2", "bins": 8, "total_weight": 2935.50, "tare_weight": 440.00, "units": "kg"},
]
crush_orders = [
    {"dockets": ["2022 Blue Grouse Pinot Noir Charles & Jacob A1", "2022 Blue Grouse Chardonnay Charles & Jacob B3", "2022 Blue Grouse Pinot Noir Paula A5"], "quantities": [140, 351, 233], "units": ["kg", "kg", "kg"],
     "vintage": 2022, "crush_type": "Whole Cluster Press", "date": "2022-09-30", "vessel_id": 2, "vessel_type": "tank", "vessel_quantity": 724},
    {"dockets": ["2022 Green Gage Farm Schönburger Brunner B5"], "quantities": [4783.50], "units": ["kg"],
     "vintage": 2022, "crush_type": "Crush & Press", "date": "2022-10-03", "vessel_id": 3, "vessel_type": "tank", "vessel_quantity": 4783.50},
    {"dockets": ["2022 Blue Grouse Siegerrebe Paula C2"], "quantities": [2495.50], "units": ["kg"],
     "vintage": 2022, "crush_type": "Crush & Press", "date": "2022-10-07", "vessel_id": 4, "vessel_type": "tank", "vessel_quantity": 2495.50},
]


try:
    for vintage in vintages:
        model = VintageChoices(choice=vintage)
        model.save()
    for varietal in varietals:
        model = VarietalChoices(choice=varietal)
        model.save()
    for vineyard in vineyards:
        model = VineyardChoices(choice=vineyard)
        model.save()
    for grower in growers:
        model = GrowerChoices(choice=grower)
        model.save()
    for block in blocks:
        model = BlockChoices(choice=block)
        model.save()
    for unit in units:
        model = UnitChoices(choice=unit)
        model.save()
    for vessel in vessels:
        model = Vessel(type_name=vessel["type_name"], type_id=vessel["type_id"], expansion_chamber_diameter=vessel["expansion_chamber_diameter"],
                       expansion_chamber_height=vessel["expansion_chamber_height"], expansion_chamber_radius=vessel["expansion_chamber_radius"],
                       tank_diameter=vessel["tank_diameter"], top_cone_height=vessel["top_cone_height"],
                       cylinder_height=vessel["cylinder_height"], cylinder_radius=vessel["cylinder_radius"],
                       floor_height=vessel["floor_height"])
        model.save()
    for crush_type in crush_types:
        model = CrushOrderTypeChoices(choice=crush_type)
        model.save()
    for docket in dockets:
        docket = Docket(vintage=docket["vintage"], grower=docket["grower"], varietal=docket["varietal"], vineyard=docket["vineyard"], block=docket["block"])
        docket.save()
    for intake in fruit_intakes:
        docket = get_object_or_None(Docket, docket_number=intake["docket"])
        fruit_intake = FruitIntake(number_of_bins=intake["bins"], total_weight=intake["total_weight"], tare_weight=intake["tare_weight"], units=intake["units"])
        fruit_intake.save()
        fruit_intake.docket = docket
        fruit_intake.save()
    for order in crush_orders:
        crush_order = CrushOrder(vintage=order["vintage"], crush_type=order["crush_type"], date=order["date"])
        crush_order.save()
        vessel = get_object_or_None(Vessel, type_name=order["vessel_type"], type_id=order["vessel_id"])
        vessel_crush_order_mapping = CrushOrderVesselMapping(crush_order=crush_order, vessel=vessel, quantity=order["vessel_quantity"], units="kg")
        vessel_crush_order_mapping.save()
        for index in range(len(order["dockets"])):
            docket = get_object_or_None(Docket, docket_number=order["dockets"][index])
            crush_mapping = CrushOrderDocketMapping(crush_order=crush_order, docket=docket, quantity=order["quantities"][index], units=order["units"][index])
            crush_mapping.save()
except django.db.utils.OperationalError:
    print("Database not yet created.")
    pass
except django.db.utils.IntegrityError:
    print("This has already run.")
    pass
except Exception as e:
    print("Failed to create the test data.")
    print(e)
    raise e
