from django import forms
from .models import PDFFile

class PDFFileForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError("No file selected!")
        
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        
        if file.content_type != 'application/pdf':
            raise forms.ValidationError("The uploaded file is not a valid PDF.")
        
        return file
