from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    menu_principal, lista_furgones, agregar_furgon, detalle_furgon, agregar_pasajero,
    ver_calendario, calendario_pasajeros, registro_conductor, redireccion_dashboard,
    dashboard_admin, dashboard_conductor,api_login
)

urlpatterns = [
    path('', menu_principal, name='menu_principal'),  # ✅ Carga el menú en la raíz
    path('menu/', menu_principal, name='menu'),  # ✅ Nueva ruta para acceder al menú
    path('furgones/', lista_furgones, name='lista_furgones'),
    path('furgones/agregar/', agregar_furgon, name='agregar_furgon'),
    path('furgones/<int:furgon_id>/', detalle_furgon, name='detalle_furgon'),
    path('furgones/<int:furgon_id>/agregar_pasajero/', agregar_pasajero, name='agregar_pasajero'),
    
    # ✅ Rutas del calendario
    path('calendario/', ver_calendario, name='ver_calendario'),
    path('calendario/datos/', calendario_pasajeros, name='calendario_pasajeros'),

    # ✅ Rutas de autenticación
    path('registro/', registro_conductor, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='furgones/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ✅ Redirección al dashboard correcto según el rol
    path('dashboard/', redireccion_dashboard, name='redireccion_dashboard'),

    # ✅ Dashboards separados
    path('admin_dashboard/', dashboard_admin, name='dashboard_admin'),  # ✅ Verifica que esta línea esté aquí
    path('conductor_dashboard/', dashboard_conductor, name='dashboard_conductor'),

    path('api/login/', api_login, name='api_login'),  # ✅ Nueva API para Postman

]
