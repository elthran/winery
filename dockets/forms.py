from datetime import datetime

from django import forms

from dockets.models import Docket, VintageChoices, VarietalChoices, VineyardChoices, Constants
import winery.constants


class FruitIntakeForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all())
    varietal = forms.ModelChoiceField(label='varietal', queryset=VarietalChoices.objects.all())
    vineyard = forms.ModelChoiceField(label='vineyard', queryset=VineyardChoices.objects.all())
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


class VarietalEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VarietalChoices.objects.all(), required=False)
    edit_value = forms.CharField(label='edit_value', max_length=100, initial="", required=False)
    new_value = forms.CharField(label='new_value', max_length=100, initial="", required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        cleaned_data = super().clean()
        new_value = self.cleaned_data.get("new_value")
        edit_value = self.cleaned_data.get("edit_value")
        existing_field = self.cleaned_data.get("existing_field")
        if not new_value and (not existing_field or not edit_value):
            raise forms.ValidationError("You must enter a field to update.")


class VintageEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VintageChoices.objects.all(), required=False)
    edit_value = forms.IntegerField(label='edit_value', required=False)
    new_value = forms.IntegerField(label='new_value', required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        cleaned_data = super().clean()
        new_value = self.cleaned_data.get("new_value")
        edit_value = self.cleaned_data.get("edit_value")
        existing_field = self.cleaned_data.get("existing_field")
        if not new_value and (not existing_field or not edit_value):
            raise forms.ValidationError("You must enter a field to update.")


class VineyardEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VineyardChoices.objects.all(), required=False)
    edit_value = forms.CharField(label='edit_value', max_length=100, initial="", required=False)
    new_value = forms.CharField(label='new_value', max_length=100, initial="", required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        cleaned_data = super().clean()
        new_value = self.cleaned_data.get("new_value")
        edit_value = self.cleaned_data.get("edit_value")
        existing_field = self.cleaned_data.get("existing_field")
        if not new_value and (not existing_field or not edit_value):
            raise forms.ValidationError("You must enter a field to update.")
