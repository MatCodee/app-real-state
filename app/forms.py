from django import forms 
from .models import ClientModel

class CreateClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['name','phone','email','message']

