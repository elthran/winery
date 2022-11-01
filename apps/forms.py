from datetime import datetime

from django import forms

from apps.models.models import Docket, FruitIntake
from apps.models.choices import VintageChoices, VarietalChoices, VineyardChoices, UnitChoices, BlockChoices, \
    GrowerChoices, CrushOrderTypeChoices, VesselChoices


class FruitIntakeInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all(), required=False)
    varietal = forms.ModelChoiceField(label='varietal', queryset=VarietalChoices.objects.all(), required=False)
    vineyard = forms.ModelChoiceField(label='vineyard', queryset=VineyardChoices.objects.all(), required=False)
    block = forms.ModelChoiceField(label='block', queryset=BlockChoices.objects.all(), required=False)
    grower = forms.ModelChoiceField(label='grower', queryset=GrowerChoices.objects.all(), required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        vintage = self.cleaned_data.get("vintage")
        vineyard = self.cleaned_data.get("vineyard")
        varietal = self.cleaned_data.get("varietal")
        block = self.cleaned_data.get("block")
        grower = self.cleaned_data.get("grower")
        if not vintage or not vineyard or not varietal or not block or not grower:
            raise forms.ValidationError("Field is missing.")


class FruitIntakeSubsequentForm(forms.Form):
    date = forms.DateTimeField(label='date', initial=datetime.now(), localize=True)
    number_of_bins = forms.IntegerField(label='number_of_bins')
    total_weight = forms.IntegerField(label='total_weight')
    tare_weight = forms.IntegerField(label='tare_weight')
    units = forms.ModelChoiceField(label='units', queryset=UnitChoices.objects.all(), initial="kg")

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        total_weight = self.cleaned_data.get("total_weight")
        tare_weight = self.cleaned_data.get("tare_weight")
        if total_weight < tare_weight:
            raise forms.ValidationError("Total weight must be greater than tare weight")
        if total_weight < 0:
            raise forms.ValidationError("Total weight must be greater than 0")
        if tare_weight < 0:
            raise forms.ValidationError("Tare weight must be greater than 0")


class CrushOrderForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all())
    crush_type = forms.ModelChoiceField(label='docket_1', queryset=CrushOrderTypeChoices.objects.all())
    docket_1 = forms.ModelChoiceField(label='docket_1', queryset=Docket.objects.all())
    docket_1_quantity = forms.IntegerField(label='docket_1_quantity')
    docket_1_units = forms.ModelChoiceField(label='docket_1_units', queryset=UnitChoices.objects.all(), initial="kg")
    docket_2 = forms.ModelChoiceField(label='docket_2', queryset=Docket.objects.all(), required=False)
    docket_2_quantity = forms.IntegerField(label='docket_2_quantity', required=False)
    docket_2_units = forms.ModelChoiceField(label='docket_2_units', queryset=UnitChoices.objects.all(), required=False,
                                            initial="kg")
    date = forms.DateTimeField(label='date', initial=datetime.now(), localize=True, required=False)

    vessel_1 = forms.ModelChoiceField(label='vessel_1', queryset=VesselChoices.objects.all(), required=False)
    vessel_1_amount = forms.IntegerField(label='vessel_1_amount', required=False)
    vessel_2 = forms.ModelChoiceField(label='vessel_2', queryset=VesselChoices.objects.all(), required=False)
    vessel_2_amount = forms.IntegerField(label='vessel_2_amount', required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        docket_1 = self.cleaned_data.get("docket_1")
        docket_1_quantity = self.cleaned_data.get("docket_1_quantity")
        docket_1_units = self.cleaned_data.get("docket_1_units")

        docket_2 = self.cleaned_data.get("docket_2")
        docket_2_quantity = self.cleaned_data.get("docket_2_quantity")
        docket_2_units = self.cleaned_data.get("docket_2_units")

        if docket_1 == docket_2:
            raise forms.ValidationError("The dockets must be different.")
        if not docket_1 or not docket_1_quantity or not docket_1_units:
            raise forms.ValidationError("Requires at least one docket.")
        if docket_2 and not (docket_2_quantity and docket_2_units):
            raise forms.ValidationError("If Docket 2 is selected, it must be fully completed.")


class VarietalEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label='existing_field', queryset=VarietalChoices.objects.all(),
                                            required=False)
    edit_value = forms.CharField(label='edit_value', max_length=100, initial="", required=False)
    new_value = forms.CharField(label='new_value', max_length=100, initial="", required=False)

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
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
