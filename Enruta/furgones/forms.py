from django import forms
from .models import Furgon, Pasajero
from django.contrib.auth.forms import UserCreationForm
from .models import Conductor

class FurgonForm(forms.ModelForm):
    class Meta:
        model = Furgon
        fields = ['patente', 'capacidad', 'conductor']

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'furgon']


class PasajeroForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Pasajero
        fields = ['nombre', 'fecha']

class PasajeroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['asistencia', 'comentario']
        widgets = {
            'asistencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RegistroConductorForm(UserCreationForm):
    class Meta:
        model = Conductor  # ✅ Usa el modelo `Conductor`
        fields = ['username', 'password1', 'password2']  # ✅ Solo nombre de usuario y contraseña

    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_conductor = True  # ✅ Todos los registrados son conductores
        user.es_admin = False  # ✅ Asegurar que no sean administradores
        if commit:
            user.save()
        return user