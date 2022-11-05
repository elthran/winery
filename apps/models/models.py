import math
from datetime import datetime

from django.db import models


class CrushOrderDocketMapping(models.Model):
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE, related_name="crush_order_docket_mappings")
    docket = models.ForeignKey('apps.Docket', on_delete=models.CASCADE, related_name="crush_order_docket_mappings")
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
    docket = models.ForeignKey('apps.Docket', on_delete=models.CASCADE, null=True, related_name="fruit_intakes")
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE, null=True, related_name="fruit_intakes")

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


class CrushOrderVesselMappings(models.Model):
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE, null=True,
                                    related_name="crush_order_vessel_mappings")
    vessel = models.ForeignKey('apps.Vessel', on_delete=models.CASCADE, null=True, related_name="crush_order_vessel_mappings")
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)
