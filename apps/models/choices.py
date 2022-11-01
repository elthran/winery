from django.db import models


class BaseChoiceModel(models.Model):
    choice = models.TextField(unique=True, null=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return u'{0}'.format(self.choice)

    def save(self, *args, **kwargs):
        if self.is_default:
            VarietalChoices.objects.filter(is_default=True).update(is_default=False)
        return super().save(*args, **kwargs)


class VintageChoices(BaseChoiceModel):
    pass


class VarietalChoices(BaseChoiceModel):
    pass


class VineyardChoices(BaseChoiceModel):
    pass


class GrowerChoices(BaseChoiceModel):
    pass


class BlockChoices(BaseChoiceModel):
    pass


class UnitChoices(BaseChoiceModel):
    pass


class VesselChoices(BaseChoiceModel):
    pass


class CrushOrderTypeChoices(BaseChoiceModel):
    pass

class Constants(models.Model):
    choice = models.TextField(unique=True, null=False)
    data_type = models.TextField(null=False)
