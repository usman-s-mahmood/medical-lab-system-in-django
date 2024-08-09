# created manually!
from django import forms
from . import models
from django.core.validators import FileExtensionValidator

class FileUploadForm(forms.ModelForm):
    upload_name = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the file for analysis'
            }
        ),
        label='Enter the file for analysis (only excel files with .xlsx are allowed)',
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'xlsx'
                ]
            )
        ]
    )
    class Meta:
        model = models.UploadedFile
        fields = ('upload_name',)
        
class SampleGenerationForm(forms.ModelForm):
    dataset_size = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the size of dataset'
            }
        ),
        label='Enter the size of dataset that you want to generate'
    )
    class Meta:
        model = models.SampleGeneration
        fields = ('dataset_size',)
        