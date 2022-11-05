import math
from datetime import datetime

from django.db import models


class Docket(models.Model):
    docket_number = models.TextField(unique=True, null=False)
    vintage = models.IntegerField(null=True)
    varietal = models.TextField(null=True)
    vineyard = models.TextField(null=True)
    block = models.TextField(null=True)
    grower = models.TextField(null=True)
    crush_orders = models.ManyToManyField('apps.CrushOrder', through='CrushOrderDocketMapping')

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