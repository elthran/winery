import math
from datetime import datetime

from django.db import models


class CrushOrder(models.Model):
    vintage = models.IntegerField(null=True)
    crush_type = models.TextField(null=True)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    dockets = models.ManyToManyField('apps.Docket', through='CrushOrderDocketMapping')
    vessels = models.ManyToManyField('apps.Vessel', through='CrushOrderVesselMapping')

    @property
    def total_weight(self):
        return sum([mapping.quantity for mapping in self.crush_order_docket_mappings.all()])

    @property
    def predicted_volume(self):
        if not self.total_weight or self.total_weight == 0:
            return "Undefined"
        if self.crush_type == "Whole Cluster Press":
            return 600 * self.total_weight / 1000
        return 650 * self.total_weight / 1000