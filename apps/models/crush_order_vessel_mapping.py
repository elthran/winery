from django.db import models


class CrushOrderVesselMapping(models.Model):
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)

    crush_order = models.ForeignKey(
        "apps.CrushOrder",
        on_delete=models.CASCADE,
        null=True,
        related_name="crush_order_vessel_mappings",
    )
    vessel = models.ForeignKey(
        "apps.Vessel",
        on_delete=models.CASCADE,
        null=True,
        related_name="crush_order_vessel_mappings",
    )
