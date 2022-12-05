from django.db import models


class Dip(models.Model):
    dip_depth = models.IntegerField(null=True)
    dip_type = models.TextField(null=True)
    vessel = models.ForeignKey('apps.Vessel', on_delete=models.CASCADE, null=True, related_name="dips")
