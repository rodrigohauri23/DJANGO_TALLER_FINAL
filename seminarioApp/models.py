from django.db import models
from django.utils import timezone

# Create your models here.
class Instituciones(models.Model):
    nombre = models.CharField(max_length=60)
    
    def __str__(self):
        return self.nombre


opciones_reserva = [
    ("Reservado", "Reservado"),
    ("Completada", "Completada"),
    ("Anulada", "Anulada"),
    ("No Asisten", "No asisten")
]

class Participante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.IntegerField()
    fecha_inscripcion = models.DateField()
    instituciones = models.ForeignKey(Instituciones, on_delete=models.CASCADE)
    hora_inscripcion = models.TimeField()
    estado = models.CharField(max_length=50, choices=opciones_reserva)
    observacion = models.CharField(max_length=50)
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.fecha_inscripcion = timezone.now().date()
            self.hora_inscripcion = timezone.now().time()
        super(Participante,self).save(*args, **kwargs)   