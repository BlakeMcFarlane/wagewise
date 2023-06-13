from django import forms
from .tax_rates import STATES


class Calculator(forms.Form):

    state=forms.ChoiceField(choices=STATES, widget=forms.Select(
        attrs={
            'class': 'input-class',
        }
    ))
    annual_income=forms.IntegerField(widget=forms.TextInput(
        attrs={
        'class':'input-class',
        'placeholder':"$50,000",
    }))


class Mortgage(forms.Form):
    purchase_price=forms.IntegerField(widget=forms.TextInput(
        attrs={
        'class':'input-class',
        'placeholder':"$350,000",
    }))
    down_payment=forms.FloatField(widget=forms.TextInput(
        attrs={
        'class':'input-class',
        'placeholder':"20%",
    }))
    interest_rate=forms.FloatField(widget=forms.TextInput(
        attrs={
        'class':'input-class',
        'placeholder':"4%",
    }))
    loan_term=forms.ChoiceField(choices=[(15,15),(30,30)], widget=forms.RadioSelect(attrs={
            'class': 'input-class',
        }))
