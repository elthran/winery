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

    #
    # @property
    # def pre_crush_weight(self):
    #     # is_null = [intake.fruit_weight or 0 for intake in self.fruit_intakes.all()]
    #     return sum([intake.fruit_weight or 0 for intake in self.fruit_intakes.all()])

    def __str__(self):
        return u'{0}'.format(self.docket_number)


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
        if self.crush_type == "Whole Cluster Press":
            return 650 / self.total_weight
        return 600 / self.total_weight


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
    type = models.TextField(null=True)
    name = models.TextField(null=True)
    crush_orders = models.ManyToManyField(CrushOrder, related_name="vessels")
