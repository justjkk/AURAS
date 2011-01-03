from django import forms

class UploadFileForm(forms.Form):
    file  = forms.FileField(help_text="Select a file of type .xls, .csv or .xml")
