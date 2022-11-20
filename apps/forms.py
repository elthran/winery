from datetime import datetime

from django import forms

from apps.models.dockets import Docket
from apps.models.choices import VintageChoices, VarietalChoices, VineyardChoices, UnitChoices, BlockChoices, \
    GrowerChoices, CrushOrderTypeChoices
from apps.models.vessels import Vessel


class FruitIntakeInitialForm(forms.Form):
    vintage = forms.ModelChoiceField(label="vintage", queryset=VintageChoices.objects.all(), required=False)
    varietal = forms.ModelChoiceField(label="varietal", queryset=VarietalChoices.objects.all(), required=False)
    vineyard = forms.ModelChoiceField(label="vineyard", queryset=VineyardChoices.objects.all(), required=False)
    block = forms.ModelChoiceField(label="block", queryset=BlockChoices.objects.all(), required=False)
    grower = forms.ModelChoiceField(label="grower", queryset=GrowerChoices.objects.all(), required=False)

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
    date = forms.DateTimeField(label="date", initial=datetime.now(), localize=True)
    number_of_bins = forms.IntegerField(label="number_of_bins")
    total_weight = forms.IntegerField(label="total_weight")
    tare_weight = forms.IntegerField(label="tare_weight")
    units = forms.ModelChoiceField(label="units", queryset=UnitChoices.objects.all(), initial="kg")

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
    vintage = forms.ModelChoiceField(label="vintage", queryset=VintageChoices.objects.all())
    crush_type = forms.ModelChoiceField(label="docket_1", queryset=CrushOrderTypeChoices.objects.all())
    date = forms.DateTimeField(label="date", localize=True, required=False, initial=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: I can't move this up to the db call because the table doesn't exist on db creation.
        self.initial["vintage"] = VintageChoices.objects.last()
        all_dockets = Docket.objects.all().order_by('-id')
        self.maximum_fields = min(5, len(all_dockets))
        for i in range(self.maximum_fields):
            docket_field_name = f"docket_{i}"
            quantity_field_name = f"docket_{i}_quantity"
            units_field_name = f"docket_{i}_units"
            vessel_field_name = f"vessel_{i}"
            vessel_amount_field_name = f"vessel_{i}_amount"

            self.fields[docket_field_name] = forms.ModelChoiceField(label=docket_field_name,
                                                                    queryset=all_dockets,
                                                                    required=False)
            self.fields[quantity_field_name] = forms.IntegerField(label=quantity_field_name,
                                                                  required=False, initial=0)
            self.fields[units_field_name] = forms.ModelChoiceField(label=units_field_name,
                                                                   queryset=UnitChoices.objects.all(),
                                                                   required=False, initial=UnitChoices.objects.last())
            self.fields[vessel_field_name] = forms.ModelChoiceField(label=f"vessel_{i}",
                                                                    queryset=Vessel.objects.all(),
                                                                    required=False)
            self.fields[vessel_amount_field_name] = forms.ModelChoiceField(label=f"vessel_{i}_amount",
                                                                           queryset=Vessel.objects.all(),
                                                                           required=False)

            if i == 0:
                self.initial[docket_field_name] = all_dockets[0]

    def clean(self):
        """
        Ensure that either they are entering a new valid integer or are updating a valid integer with a valid integer.
        """
        i = 0
        human_readable_count_mapper = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth", 5: "sixth"}
        used_dockets = []
        while i < self.maximum_fields:
            docket = self.cleaned_data.get(f"docket_{i}")
            quantity = self.cleaned_data.get(f"docket_{i}_quantity")
            units = self.cleaned_data.get(f"docket_{i}_units")
            vessel = self.cleaned_data.get(f"vessel_{i}")
            vessel_amount = self.cleaned_data.get(f"vessel_{i}_amount")
            if docket and (not quantity or not units):
                raise forms.ValidationError(f"The {human_readable_count_mapper[i]} docket is not complete.")
            if i == 0 and not docket:
                raise forms.ValidationError("Requires at least one docket.")
            if not docket:
                break
            if docket in used_dockets:
                raise forms.ValidationError("The dockets must be different.")
            else:
                used_dockets.append(docket)
            if quantity <= 0:
                raise forms.ValidationError(f"The quantity must be greater than 0.")
            i += 1


class VarietalEntryForm(forms.Form):
    existing_field = forms.ModelChoiceField(label="existing_field", queryset=VarietalChoices.objects.all(),
                                            required=False)
    edit_value = forms.CharField(label="edit_value", max_length=100, initial="", required=False)
    new_value = forms.CharField(label="new_value", max_length=100, initial="", required=False)

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
    existing_field = forms.ModelChoiceField(label="existing_field", queryset=VintageChoices.objects.all(),
                                            required=False)
    edit_value = forms.IntegerField(label="edit_value", required=False)
    new_value = forms.IntegerField(label="new_value", required=False)

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
    existing_field = forms.ModelChoiceField(label="existing_field", queryset=VineyardChoices.objects.all(),
                                            required=False)
    edit_value = forms.CharField(label="edit_value", max_length=100, initial="", required=False)
    new_value = forms.CharField(label="new_value", max_length=100, initial="", required=False)
    merging_field = forms.ModelChoiceField(label="merging_field", queryset=VineyardChoices.objects.all(),
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
