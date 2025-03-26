from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Furgon, Pasajero, Conductor
from .forms import FurgonForm, PasajeroForm, PasajeroAsistenciaForm, RegistroConductorForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def menu_principal(request):
    """ Redirige a los conductores a su propio dashboard y muestra el dashboard admin en menu.html """
    if request.user.es_conductor:
        return redirect('dashboard_conductor')  # ✅ Redirigir a conductores a su panel

    # ✅ Si el usuario es administrador, calcular estadísticas y mostrar el dashboard
    total_furgones = Furgon.objects.count()
    pasajeros_hoy = Pasajero.objects.filter(fecha=date.today()).count()
    furgones_en_servicio = Furgon.objects.filter(pasajeros__fecha=date.today()).distinct().count()

    context = {
        'total_furgones': total_furgones,
        'pasajeros_hoy': pasajeros_hoy,
        'furgones_en_servicio': furgones_en_servicio,
    }
    return render(request, 'furgones/menu.html', context)

# Ver calendario
def ver_calendario(request):
    return render(request, 'furgones/calendario.html')

# Vista para la lista de furgones
@login_required
def lista_furgones(request):
    furgones = Furgon.objects.all()
    return render(request, 'furgones/lista_furgones.html', {'furgones': furgones})

# Agregar un nuevo furgón
@login_required
def agregar_furgon(request):
    if request.method == "POST":
        form = FurgonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_furgones')
    else:
        form = FurgonForm()
    return render(request, 'furgones/agregar_furgon.html', {'form': form})

# Detalles de un furgón (Pasajeros + Asistencia)
@login_required
def detalle_furgon(request, furgon_id):
    furgon = get_object_or_404(Furgon, id=furgon_id)
    pasajeros = furgon.pasajeros.all()

    if request.method == "POST":
        pasajero_id = request.POST.get('pasajero_id')
        pasajero = get_object_or_404(Pasajero, id=pasajero_id)
        form = PasajeroAsistenciaForm(request.POST, instance=pasajero)

        if form.is_valid():
            form.save()
            return redirect('detalle_furgon', furgon_id=furgon.id)

    return render(request, 'furgones/detalle_furgon.html', {'furgon': furgon, 'pasajeros': pasajeros, 'form': PasajeroAsistenciaForm()})

# Agregar pasajero a un furgón
@login_required
def agregar_pasajero(request, furgon_id):
    furgon = get_object_or_404(Furgon, id=furgon_id)

    if request.method == "POST":
        form = PasajeroForm(request.POST)
        if form.is_valid():
            pasajero = form.save(commit=False)
            pasajero.furgon = furgon
            pasajero.save()
            return redirect('lista_furgones')

    else:
        form = PasajeroForm(initial={'fecha': date.today()})  # Fecha predeterminada: hoy

    return render(request, 'furgones/agregar_pasajero.html', {'form': form, 'furgon': furgon})

# Calendario de pasajeros
@login_required
def calendario_pasajeros(request):
    pasajeros = Pasajero.objects.all()
    eventos = [
        {"title": pasajero.nombre, "start": pasajero.fecha.strftime("%Y-%m-%d")}
        for pasajero in pasajeros
    ]
    return JsonResponse(eventos, safe=False)

# Vista de Registro para Conductores
def registro_conductor(request):
    """ Registra un conductor y lo redirige a su dashboard """
    if request.method == "POST":
        form = RegistroConductorForm(request.POST)
        if form.is_valid():
            conductor = form.save(commit=False)  # ✅ No guardamos aún
            conductor.es_conductor = True  # ✅ Marcamos que es conductor
            conductor.is_staff = False  # ✅ Aseguramos que NO sea admin
            conductor.is_superuser = False  # ✅ No es superusuario
            conductor.save()  # ✅ Ahora sí guardamos
            login(request, conductor)  # ✅ Inicia sesión automáticamente
            return redirect('dashboard_conductor')  # ✅ Redirige al dashboard de conductores
    else:
        form = RegistroConductorForm()
    return render(request, 'furgones/registro.html', {'form': form})


# 🔹 REDIRECCIÓN AUTOMÁTICA AL DASHBOARD CORRECTO SEGÚN ROL
@login_required
def redireccion_dashboard(request):
    """ Redirige al usuario a su dashboard según su rol """
    if getattr(request.user, 'es_admin', True):  # ✅ Si tiene 'es_admin', verifica su valor
        return redirect('menu')  # ✅ Dashboard del admin
    elif getattr(request.user, 'es_conductor', False):  # ✅ Si tiene 'es_conductor'
        return redirect('dashboard_conductor')  # ✅ Redirigir a conductores
    return redirect('login')  # ✅ Si no es ninguno, lo manda al login

# Dashboard para Administradores
@login_required
def dashboard_admin(request):
    """ Muestra el panel de administración dentro de `menu.html` """
    if not request.user.es_admin:
        return redirect('dashboard_conductor')  # ✅ Redirigir a conductores si intentan acceder

    total_furgones = Furgon.objects.count()
    pasajeros_hoy = Pasajero.objects.filter(fecha=date.today()).count()
    furgones_en_servicio = Furgon.objects.filter(pasajeros__fecha=date.today()).distinct().count()

    # 🔹 Agregar datos de asistencia
    total_asistencias = Pasajero.objects.filter(fecha=date.today(), asistencia=True).count()
    total_no_asistencias = Pasajero.objects.filter(fecha=date.today(), asistencia=False).count()

    context = {
        'total_furgones': total_furgones,
        'pasajeros_hoy': pasajeros_hoy,
        'furgones_en_servicio': furgones_en_servicio,
        'total_asistencias': total_asistencias,
        'total_no_asistencias': total_no_asistencias,
    }
    return render(request, 'furgones/menu.html', context)

# Dashboard para Conductores
@login_required
def dashboard_conductor(request):
    if not request.user.es_conductor:
        return redirect('dashboard_admin')

    furgones = request.user.furgones.all()
    pasajeros_hoy = Pasajero.objects.filter(furgon__in=furgones, fecha=date.today())

    if request.method == "POST":
        pasajero_id = request.POST.get('pasajero_id')
        pasajero = get_object_or_404(Pasajero, id=pasajero_id)

        asistencia = 'asistencia' in request.POST  # ✅ Si está marcado, devuelve True
        comentario = request.POST.get('comentario', '')  # ✅ Captura el comentario

        pasajero.asistencia = asistencia
        pasajero.comentario = comentario
        pasajero.save()

        return redirect('dashboard_conductor')  # ✅ Recarga la página después de guardar

    return render(request, 'furgones/dashboard_conductor.html', {'pasajeros_hoy': pasajeros_hoy})


@csrf_exempt  # 🔹 Evita el error CSRF en Postman
def api_login(request):
    """ API para autenticación en Postman """
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login exitoso", "username": user.username, "es_conductor": user.es_conductor, "es_admin": user.es_admin}, status=200)
        else:
            return JsonResponse({"error": "Credenciales incorrectas"}, status=401)

    return JsonResponse({"error": "Método no permitido"}, status=405)
