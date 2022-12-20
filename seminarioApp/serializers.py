from rest_framework import serializers
from .models import Participante
from .models import Instituciones

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'
        
        
class InstitucionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituciones
        fields = '__all__'


