from datetime import datetime

from django import forms

from dockets.models import Docket
import winery.constants


class FruitIntakeForm(forms.Form):
    vintage = forms.ChoiceField(label='vintage', choices=winery.constants.YEAR_CHOICES)
    varietal = forms.ChoiceField(label='varietal', choices=winery.constants.VARIETAL_CHOICES)
    vineyard = forms.ChoiceField(label='vineyard', choices=winery.constants.VINEYARD_CHOICES)
    block = forms.IntegerField(label='block', initial=1)
    grower = forms.CharField(label='grower', max_length=100, initial="unknown")
    date = forms.DateTimeField(label='date', initial=datetime.now(), localize=True)
    # number_of_bins = forms.CharField(label='number_of_bins', max_length=100)
    # total_weight_kg = forms.CharField(label='total_weight_kg', max_length=100)
    # total_weight_display_unit = forms.CharField(label='total_weight_display_unit', max_length=100)
    # tare_weight_kg = forms.CharField(label='tare_weight_kg', max_length=100)
    # tare_weight_display_unit = forms.CharField(label='tare_weight_display_unit', max_length=100)


class CrushOrderForm(forms.Form):
    vintage = forms.ChoiceField(label='vintage', choices=winery.constants.YEAR_CHOICES)
    docket_number = forms.CharField(label='docket_number', max_length=100)

    def clean_docket_number(self):
        form_docket_number = self.cleaned_data.get("docket_number")
        existing = Docket.objects.filter(docket_number=form_docket_number).exists()
        if not existing:
            raise forms.ValidationError("Docket Number does not exist in database")
        return form_docket_number
