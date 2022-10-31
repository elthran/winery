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

    def __str__(self):
        return u'{0}'.format(self.docket_number)


class CrushOrder(models.Model):
    vintage = models.IntegerField(null=True)
    dockets = models.TextField(null=True)
    quantity = models.IntegerField(null=True)


class FruitIntake(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    number_of_bins = models.IntegerField(null=True)
    total_weight = models.IntegerField(null=True)
    tare_weight = models.IntegerField(null=True)
    units = models.TextField(null=True)
    docket = models.ForeignKey(Docket, on_delete=models.CASCADE, null=True)
    crush_order = models.ForeignKey(CrushOrder, on_delete=models.CASCADE, null=True)

    @property
    def docket_number(self):
        return f'{self.vintage}{self.vineyard}{self.varietal}{self.block}'.replace(" ", "")

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

    def __str__(self):
        return u'{0}'.format(self.docket_number)

