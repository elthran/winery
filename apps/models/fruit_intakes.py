from datetime import datetime

from django.db import models


class FruitIntake(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    number_of_bins = models.IntegerField(null=True)
    total_weight = models.IntegerField(null=True)
    tare_weight = models.IntegerField(null=True)
    units = models.TextField(null=True)
    docket = models.ForeignKey('apps.Docket', on_delete=models.CASCADE, null=True, related_name="fruit_intakes")
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE, null=True,
                                    related_name="fruit_intakes")

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
