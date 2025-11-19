# apps/core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# --- IMPORTANTE: Importamos el modelo para poder buscar datos ---
from .models import Condominio

# --- INICIO: Vistas del Dashboard ---

@login_required
def index_view(request):
    """
    Vista principal (Dashboard).
    Ahora recupera los condominios de la base de datos.
    """
    
    # 1. Buscamos TODOS los condominios en la base de datos
    lista_condominios = Condominio.objects.all()

    # 2. Preparamos el contexto con el usuario Y la lista
    contexto = {
        'usuario': request.user,
        'mis_condominios': lista_condominios  # <--- Enviamos la lista al HTML
    }
    
    return render(request, 'index.html', contexto)

# --- FIN: Vistas del Dashboard ---