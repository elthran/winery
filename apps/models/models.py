import math
from datetime import datetime

from django.db import models


# Create your models here.
class Docket(models.Model):
    docket_number = models.TextField(unique=True, null=False)
    vintage = models.IntegerField(null=True)
    varietal = models.TextField(null=True)
    vineyard = models.TextField(null=True)
    block = models.TextField(null=True)
    grower = models.TextField(null=True)

    def save(self, *args, **kwargs):
        """Overwrite the save function for this model"""
        self.docket_number = f'{self.vintage} {self.grower} {self.varietal} {self.vineyard} {self.block}'
        super(Docket, self).save(*args, **kwargs)

    @property
    def fruit_weight(self):
        # is_null = [intake.fruit_weight or 0 for intake in self.fruit_intakes.all()]
        return sum([intake.fruit_weight or 0 for intake in self.fruit_intakes.all()])

    # @property
    # def uncrushed_weight(self):
        # return self.fruit_weight - self.crushed_weight (from all crush orders)

    #
    # @property
    # def pre_crush_weight(self):
    #     # is_null = [intake.fruit_weight or 0 for intake in self.fruit_intakes.all()]
    #     return sum([intake.fruit_weight or 0 for intake in self.fruit_intakes.all()])

    def __str__(self):
        return u'{0} - {1}'.format(self.docket_number, self.fruit_weight)


class CrushOrder(models.Model):
    vintage = models.IntegerField(null=True)
    crush_type = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)

    # crush_mappings = models.ManyToOneRel(CrushMapping)

    @property
    def total_weight(self):
        return sum([mapping.quantity for mapping in self.crush_mappings.all()])

    @property
    def predicted_volume(self):
        if not self.total_weight or self.total_weight == 0:
            return "Undefined"
        if self.crush_type == "Whole Cluster Press":
            return 600 * self.total_weight / 1000
        return 650 * self.total_weight / 1000


class CrushMapping(models.Model):
    crush_order = models.ForeignKey(CrushOrder, on_delete=models.CASCADE, null=True, related_name="crush_mappings")
    docket = models.ForeignKey(Docket, on_delete=models.CASCADE, null=True, related_name="crush_mappings")
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)

    @property
    def percentage(self):
        return int(100.0 * self.quantity / self.crush_order.total_weight)


class FruitIntake(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    number_of_bins = models.IntegerField(null=True)
    total_weight = models.IntegerField(null=True)
    tare_weight = models.IntegerField(null=True)
    units = models.TextField(null=True)
    docket = models.ForeignKey(Docket, on_delete=models.CASCADE, null=True, related_name="fruit_intakes")
    crush_order = models.ForeignKey(CrushOrder, on_delete=models.CASCADE, null=True, related_name="fruit_intakes")

    @property
    def fruit_weight(self):
        if self.total_weight and self.tare_weight:
            return self.total_weight - self.tare_weight
        else:
            return None

    @property
    def clean_date(self):
        if not self.date:
            return None
        return self.date.date()

    # def __str__(self):
    #     return u'{0}'.format(self.docket_number)


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

    @property
    def name(self):
        return f"{self.type_name} {self.type_id}"

    @property
    def volume(self):
        if not self.cylinder_radius or not self.cylinder_height:
            return "Unknown"
        area = math.pi * self.cylinder_radius ** 2
        volume = area * self.cylinder_height
        return int(volume)

    def __str__(self):
        return u'{0}'.format(self.name)


class CrushOrderVesselMappings(models.Model):
    crush_order = models.ForeignKey(CrushOrder, on_delete=models.CASCADE, null=True,
                                    related_name="crush_order_vessel_mappings")
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, null=True, related_name="crush_order_vessel_mappings")
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)
