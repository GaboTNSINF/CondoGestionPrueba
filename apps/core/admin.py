# Importamos el módulo 'admin' de Django
from django.contrib import admin
# Importamos los modelos que hemos creado en 'core'
from .models import CatTipoCuenta, Condominio, CatPlan, Suscripcion

# --- INICIO: Admin para CatTipoCuenta ---

@admin.register(CatTipoCuenta)
class CatTipoCuentaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el catálogo de Tipos de Cuenta.
    """
    # Campos a mostrar en la lista
    list_display = ('id_tipo_cuenta', 'codigo', 'nombre')
    # Campos por los que se puede buscar
    search_fields = ('codigo', 'nombre')
    # Orden por defecto
    ordering = ('id_tipo_cuenta',)

# --- FIN: Admin para CatTipoCuenta ---


# --- INICIO: Admin para Condominio ---

@admin.register(Condominio)
class CondominioAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Condominio.
    """
    # Campos a mostrar en la lista de condominios
    list_display = ('id_condominio', 'nombre', 'rut_base', 'email_contacto', 'telefono')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'rut_base', 'email_contacto')
    
    # Filtros que aparecerán en la barra lateral
    list_filter = ('region', 'comuna')
    
    # Organiza los campos de edición en secciones (fieldsets)
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', ('rut_base', 'rut_dv'))
        }),
        ('Ubicación y Contacto', {
            'fields': ('direccion', 'comuna', 'region', 'email_contacto', 'telefono')
        }),
        ('Datos Bancarios', {
            'fields': ('banco', 'id_tipo_cuenta', 'num_cuenta')
        }),
    )
    
    # Orden por defecto
    ordering = ('nombre',)

# --- FIN: Admin para Condominio ---


# --- INICIO: Admin para CatPlan --- ¡NUEVO! ---

@admin.register(CatPlan)
class CatPlanAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el Catálogo de Planes SaaS.
    """
    list_display = (
        'nombre', 
        'codigo', 
        'precio_base_mensual', 
        'max_condominios', 
        'max_unidades', 
        'es_personalizable'
    )
    search_fields = ('nombre', 'codigo')
    list_filter = ('es_personalizable',)
    ordering = ('precio_base_mensual',)

# --- FIN: Admin para CatPlan ---


# --- INICIO: Admin para Suscripcion --- ¡NUEVO! ---

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para las Suscripciones de los usuarios.
    """
    list_display = (
        'id_usuario', 
        'id_plan', 
        'estado', 
        'monto_mensual_final', 
        'fecha_termino'
    )
    search_fields = (
        'id_usuario__email', 
        'id_usuario__nombres', 
        'id_plan__nombre'
    )
    list_filter = ('estado', 'id_plan')
    
    # Usamos 'raw_id_fields' para el 'id_usuario' porque pueden
    # haber miles de usuarios, y un dropdown sería muy lento.
    raw_id_fields = ('id_usuario',)
    
    ordering = ('id_usuario__email',)

# --- FIN: Admin para Suscripcion ---