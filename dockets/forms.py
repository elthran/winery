from django import forms


class FruitIntakeForm(forms.Form):
    varietal = forms.CharField(label='varietal', max_length=100)
    vineyard = forms.CharField(label='vineyard', max_length=100)
    block = forms.CharField(label='block', max_length=100)


class CrushOrderForm(forms.Form):
    vintage = forms.CharField(label='vintage', max_length=100)
    docket_number = forms.CharField(label='docket_number', max_length=100)
