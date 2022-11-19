from django.db import models


class CrushOrderDocketMapping(models.Model):
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE,
                                    related_name="crush_order_docket_mappings")
    docket = models.ForeignKey('apps.Docket', on_delete=models.CASCADE,
                               related_name="crush_order_docket_mappings")
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)

    @property
    def percentage(self):
        return int(100.0 * self.quantity / self.crush_order.total_weight)


class CrushOrderVesselMapping(models.Model):
    crush_order = models.ForeignKey('apps.CrushOrder', on_delete=models.CASCADE, null=True,
                                    related_name="crush_order_vessel_mappings")
    vessel = models.ForeignKey('apps.Vessel', on_delete=models.CASCADE, null=True,
                               related_name="crush_order_vessel_mappings")
    quantity = models.IntegerField(null=True)
    units = models.TextField(null=True)
