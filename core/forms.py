from django import forms

class CommandForm(forms.Form):
    command = forms.CharField(label='Enter Command', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
