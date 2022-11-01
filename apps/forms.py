from datetime import datetime

from django import forms

from apps.models.models import Docket, FruitIntake
from apps.models.choices import VintageChoices, VarietalChoices, VineyardChoices, UnitChoices, BlockChoices, \
    GrowerChoices, CrushOrderTypeChoices


class FruitIntakeInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all(), required=False)
    varietal = forms.ModelChoiceField(label='varietal', queryset=VarietalChoices.objects.all(), required=False)
    vineyard = forms.ModelChoiceField(label='vineyard', queryset=VineyardChoices.objects.all(), required=False)
    block = forms.ModelChoiceField(label='block', queryset=BlockChoices.objects.all(), required=False)
    grower = forms.ModelChoiceField(label='grower', queryset=GrowerChoices.objects.all(), required=False)

    # def clean(self):
    #     """
    #     Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
    #     """
    #     vintage = self.cleaned_data.get("vintage").choice
    #     vineyard = self.cleaned_data.get("vineyard").choice
    #     varietal = self.cleaned_data.get("varietal").choice
    #     block = self.cleaned_data.get("block").choice
    #     if get_object_or_None(FruitIntake, vintage=vintage, vineyard=vineyard, varietal=varietal, block=block):
    #         raise forms.ValidationError("Docket already exists")


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


class CrushOrderInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label='vintage', queryset=VintageChoices.objects.all())
    crush_type = forms.ModelChoiceField(label='docket_1', queryset=CrushOrderTypeChoices.objects.all())
    docket_1 = forms.ModelChoiceField(label='docket_1', queryset=Docket.objects.all())
    docket_1_quantity = forms.IntegerField(label='docket_1_quantity')
    docket_1_units = forms.ModelChoiceField(label='docket_1_units', queryset=UnitChoices.objects.all(), initial="kg")
    docket_2 = forms.ModelChoiceField(label='docket_2', queryset=Docket.objects.all(), required=False)
    docket_2_quantity = forms.IntegerField(label='docket_2_quantity', required=False)
    docket_2_units = forms.ModelChoiceField(label='docket_2_units', queryset=UnitChoices.objects.all(), required=False,
                                            initial="kg")

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        docket_1 = self.cleaned_data.get("docket_1")
        docket_2 = self.cleaned_data.get("docket_2")
        if docket_1 == docket_2:
            print("The dockets must be different")
            raise forms.ValidationError("The dockets must be different")


class CrushOrderSubsequentForm(forms.Form):
    date = forms.DateTimeField(label='date', initial=datetime.now(), localize=True)


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
