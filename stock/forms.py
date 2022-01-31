from django import forms
from stock.models import Profile, Asset

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []

class add_asset_form(forms.ModelForm):
    name = forms.CharField(label=("Ticker symbol:"))
    quantity = forms.FloatField(label=("Number of shares purchased"),min_value=0.0)

    class Meta:
        model = Asset
        fields = ['name', 'quantity']

class remove_asset_form(forms.ModelForm):

    name = forms.CharField(label=("Ticker symbol:"))
    quantity = forms.FloatField(label=("Number of shares sold"),min_value=0.0,required = False)
    class Meta:
        model = Asset
        fields = ['name', 'quantity']
