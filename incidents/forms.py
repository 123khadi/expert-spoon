from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['language', 'phone']
        widgets = {
            'language': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'WhatsApp number'}),
        }
class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'latitude', 'longitude', 'severity', 'description']
        widgets = {
            'title': forms.Select(choices=Incident.INCIDENT_TYPES, attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '34.2012'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '72.0525'}),
            'severity': forms.Select(choices=Incident.SEVERITY_CHOICES, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Incident ki tafseel likhein...'}),
        }
        from django import forms
from django.core.validators import RegexValidator
from .models import Incident

# Correct validator name (no underscore)
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Enter a valid Pakistan phone number (e.g., 03325710034 or +923325710034)"
)

class IncidentForm(forms.ModelForm):
    phone = forms.CharField(
        validators=[phone_validator],
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'WhatsApp number (optional)'}),
    )

    class Meta:
        model = Incident
        fields = ['title', 'description', 'latitude', 'longitude', 'severity', 'phone']
