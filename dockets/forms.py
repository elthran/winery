from datetime import datetime

from django import forms

from dockets.models.models import Docket
from dockets.models.choices import VintageChoices, VarietalChoices, VineyardChoices, UnitChoices, BlockChoices, \
    GrowerChoices
import winery.constants


class FruitIntakeInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all(), required=False)
    varietal = forms.ModelChoiceField(label='varietal', queryset=VarietalChoices.objects.all(), required=False)
    vineyard = forms.ModelChoiceField(label='vineyard', queryset=VineyardChoices.objects.all(), required=False)
    block = forms.ModelChoiceField(label='block', queryset=BlockChoices.objects.all(), required=False)
    grower = forms.ModelChoiceField(label='grower', queryset=GrowerChoices.objects.all(), required=False)


class FruitIntakeSubsequentForm(forms.Form):
    date = forms.DateTimeField(label='date', initial=datetime.now(), localize=True)
    number_of_bins = forms.IntegerField(label='number_of_bins')
    total_weight = forms.IntegerField(label='total_weight')
    tare_weight = forms.IntegerField(label='tare_weight')
    units = forms.ModelChoiceField(label='units', queryset=UnitChoices.objects.all())


class CrushOrderInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all(), required=False)
    docket_number = forms.ModelChoiceField(label='docket_number', queryset=Docket.objects.all(), required=False)
    quantity = forms.IntegerField(label='quantity')
    units = forms.ModelChoiceField(label='units', queryset=UnitChoices.objects.all())

class CrushOrderSubsequentForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all(), required=False)
    docket_number = forms.ModelChoiceField(label='docket_number', queryset=Docket.objects.all(), required=False)
    quantity = forms.IntegerField(label='quantity')
    units = forms.ModelChoiceField(label='units', queryset=UnitChoices.objects.all())


class VarietalEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VarietalChoices.objects.all(),
                                            required=False)
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
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VintageChoices.objects.all(),
                                            required=False)
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
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VineyardChoices.objects.all(),
                                            required=False)
    edit_value = forms.CharField(label='edit_value', max_length=100, initial="", required=False)
    new_value = forms.CharField(label='new_value', max_length=100, initial="", required=False)
    merging_field = forms.ModelChoiceField(label='merging_field', queryset=VineyardChoices.objects.all(),
                                           required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        cleaned_data = super().clean()
        new_value = self.cleaned_data.get("new_value")
        edit_value = self.cleaned_data.get("edit_value")
        existing_field = self.cleaned_data.get("existing_field")
        merging_field = self.cleaned_data.get("merging_field")
        if not new_value and (not existing_field or not edit_value):
            raise forms.ValidationError("You must enter a field to update.")
