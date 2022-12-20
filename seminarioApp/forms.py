from dataclasses import fields
from socket import fromshare
from django import forms
from .models import Participante

class FormParticipantes(forms.ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'
        widgets = {
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['hora_inscripcion']
        
