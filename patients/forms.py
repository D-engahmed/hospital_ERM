from django import forms
from .models import Appointment
from datetime import date


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['summary', 'description', 'start_date', 'time']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_start_date(self):
        d = self.cleaned_data['start_date']
        if d < date.today():
            raise forms.ValidationError('Appointment date cannot be in the past.')
        return d
