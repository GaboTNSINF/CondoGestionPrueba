# apps/usuarios/urls.py

# Importamos 'path' para definir rutas
from django.urls import path
# Importamos las vistas de autenticación que Django ya trae
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- INICIO: Rutas de Autenticación ---

    # /auth/login/
    path(
        'login/', 
        auth_views.LoginView.as_view(), 
        name='login'
    ),

    # /auth/logout/
    path(
        'logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'
    ),

    # --- FIN: Rutas de Autenticación ---
]