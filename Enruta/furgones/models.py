from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import date


class Conductor(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    es_admin = models.BooleanField(default=False)  # Identifica si es administrador
    es_conductor = models.BooleanField(default=True)  # Identifica si es conductor

    # ✅ Evitar conflictos con Django agregando `related_name`
    groups = models.ManyToManyField(Group, related_name="conductor_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="conductor_permissions", blank=True)

    def __str__(self):
        return self.username


class Furgon(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    capacidad = models.IntegerField()
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, related_name="furgones")

    def __str__(self):
        return f"{self.patente} - {self.conductor.username}"

class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(default=date.today)
    furgon = models.ForeignKey(Furgon, on_delete=models.CASCADE, related_name="pasajeros")
    asistencia = models.BooleanField(default=False)  # ✅ Nuevo campo de asistencia
    comentario = models.TextField(blank=True, null=True)  # ✅ Opcional: comentario del conductor

    def __str__(self):
        return f"{self.nombre} ({self.fecha}) - {'Asistió' if self.asistencia else 'No asistió'}"

