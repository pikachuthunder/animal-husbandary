
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'date_of_birth']

class UploadFileForm(forms.ModelForm):
    file = forms.FileField()


