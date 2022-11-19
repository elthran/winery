import math
from datetime import datetime

from django.db import models


class Vessel(models.Model):
    type_name = models.TextField(null=True)
    type_id = models.TextField(null=True)
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
        return [crush_order.vintage for crush_order in self.crush_orders.all()]

    @property
    def percentages(self):
        percentages = []
        for crush_order in self.crush_orders.all():
            docket_mappings = crush_order.crush_order_docket_mappings.all()
            for mapping in docket_mappings:
                percentages.append(mapping.percentage)
        return percentages

    @property
    def current_weight(self):
        return sum([crush_order.total_weight for crush_order in self.crush_orders.all()])

    @property
    def max_volume(self):
        if not self.cylinder_radius or not self.cylinder_height:
            return "Unknown"
        area = math.pi * self.cylinder_radius ** 2
        volume = area * self.cylinder_height
        return int(volume)

    def __str__(self):
        return u'{0}'.format(self.name)