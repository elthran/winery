from django import forms

class FruitIntakeForm(forms.Form):
    varietal = forms.CharField(label='varietal', max_length=100)
    vineyard = forms.CharField(label='vineyard', max_length=100)
    block = forms.CharField(label='block', max_length=100)
