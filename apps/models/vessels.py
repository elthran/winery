import math

from django.db import models


class Vessel(models.Model):
    type_name = models.TextField(null=True)
    type_id = models.IntegerField(null=True)
    expansion_chamber_diameter = models.FloatField(null=True)
    expansion_chamber_height = models.FloatField(null=True)
    expansion_chamber_radius = models.FloatField(null=True)
    tank_diameter = models.FloatField(null=True)
    top_cone_height = models.FloatField(null=True)
    cylinder_height = models.FloatField(null=True)
    cylinder_radius = models.FloatField(null=True)
    floor_height = models.FloatField(null=True)
    crush_orders = models.ManyToManyField('apps.CrushOrder', through='CrushOrderVesselMapping')

    @property
    def name(self):
        return f"{self.type_name} {self.type_id}"

    @property
    def vintages(self):
        return set(sorted([crush_order.vintage for crush_order in self.crush_orders.all()]))

    @property
    def docket_mappings(self):
        docket_mappings = []
        for crush_order in self.crush_orders.all():
            for docket_mapping in crush_order.crush_order_docket_mappings.all():
                docket_mappings.append(docket_mapping)
        return docket_mappings

    @property
    def crush_order_mappings(self):
        crush_order_mappings = []
        for mapping in self.crush_order_vessel_mappings.all():
            crush_order_mappings.append(mapping)
        return crush_order_mappings

    @property
    def percentages(self):
        return [round(100 * mapping.quantity / self.current_weight, 1) for mapping in self.docket_mappings]

    @property
    def weights(self):
        return [mapping.quantity for mapping in self.docket_mappings]

    @property
    def current_weight(self):
        return sum([crush_order.total_weight for crush_order in self.crush_orders.all()])

    @property
    def expansion_chamber_volume(self):
        if self.type_name == "Tank":
            area = math.pi * self.cylinder_radius ** 2
            volume = area * self.cylinder_height / 10000
            return int(volume)
        else:
            return 0

    @property
    def max_volume(self):
        if self.type_name == "Tank":
            area = math.pi * self.cylinder_radius ** 2
            volume = area * self.cylinder_height / 1000
            return "{:,}".format(int(volume - self.expansion_chamber_volume))
        else:
            return f"Unknown vessel {self.type_name}"
        # 4,725.07 - 3 and 17

    def __str__(self):
        return u'{0}'.format(self.name)