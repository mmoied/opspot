from django import forms
import datetime
class CredentialForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))

    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))

