from datetime import datetime

from django.db import models


class Constants(models.Model):
    choice = models.TextField(unique=True, null=False)
    data_type = models.TextField(null=False)


class VintageChoices(models.Model):
    choice = models.IntegerField(unique=True, null=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return u'{0}'.format(self.choice)


class VarietalChoices(models.Model):
    choice = models.TextField(unique=True, null=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return u'{0}'.format(self.choice)

    def save(self, *args, **kwargs):
        if self.is_default:
            VarietalChoices.objects.filter(is_default=True).update(is_default=False)
        return super().save(*args, **kwargs)


class VineyardChoices(models.Model):
    choice = models.TextField(unique=True, null=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return u'{0}'.format(self.choice)


# Create your models here.
class Docket(models.Model):
    docket_number = models.TextField(unique=True, null=False)
    vintage = models.IntegerField(null=True)
    varietal = models.TextField(null=False)
    vineyard = models.TextField(null=False)
    block = models.TextField(null=False)
    grower = models.TextField(null=False)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    number_of_bins = models.IntegerField(null=True)
    total_weight_kg = models.IntegerField(null=True)
    total_weight_display_unit = models.IntegerField(null=True)
    tare_weight_kg = models.IntegerField(null=True)
    tare_weight_display_unit = models.IntegerField(null=True)
    actual_volume = models.IntegerField(null=True)
    order_id = models.TextField(null=True)


class Vessel(models.Model):
    dockets = models.ManyToManyField(Docket)
    bricks = models.IntegerField()
    ph = models.IntegerField()
    tartaric_acid = models.IntegerField()
    yan = models.IntegerField()
    dap_needs = models.IntegerField()
    comments = models.TextField(null=False)
    temperature = models.IntegerField()


class Order(models.Model):
    dockets = models.ManyToManyField(Docket)
    vessel_id = models.IntegerField()
