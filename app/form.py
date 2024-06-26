from django import forms

class signature_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "w-100 ps-2", 'type' : 'text', 'placeholder' : 'Name of Authorized Person'}), required=True)
    sign = forms.FileField(widget=forms.FileInput(attrs={'class': "w-100 ps-2", 'type' : 'file', 'placeholder' : 'Upload Authorized Signature'}), required=True)

