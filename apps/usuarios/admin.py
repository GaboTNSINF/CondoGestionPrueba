# Importamos el módulo 'admin' de Django
from django.contrib import admin
# Importamos el modelo UserAdmin base, que ya sabe cómo mostrar usuarios
from django.contrib.auth.admin import UserAdmin
# Importamos nuestro modelo Usuario personalizado
from .models import Usuario

# --- INICIO: Configuración del Admin para Usuario ---

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Esta clase le dice a Django cómo queremos mostrar y administrar
    nuestro modelo 'Usuario' en el panel de /admin.
    
    Heredamos de 'UserAdmin' porque ya tiene resuelta
    la mayoría de la lógica (como el cambio de contraseña, permisos, etc.).
    """
    
    # ¿Recuerdas los campos ('nombres', 'apellidos', etc.) que definimos
    # en el 'UsuarioManager' para el 'createsuperuser'?
    # Aquí tenemos que decirle al /admin qué campos mostrar al CREAR un usuario.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rut_base', 'rut_dv', 'nombres', 'apellidos', 'tipo_usuario')}),
    )

    # Y aquí le decimos qué campos mostrar al EDITAR un usuario.
    # 'fieldsets' SOBREESCRIBE la configuración base.
    fieldsets = (
        # El primer bloque es 'None' (sin título) y muestra el email y password
        (None, {'fields': ('email', 'password')}),
        
        # El segundo bloque se titula 'Información Personal'
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'rut_base', 'rut_dv', 'telefono', 'direccion')}),
        
        # El tercer bloque es 'Permisos'
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'tipo_usuario', 'groups', 'user_permissions')}),
        
        # El cuarto bloque es 'Fechas Importantes'
        ('Fechas Importantes', {'fields': ('last_login', 'creado_at')}),
    )

    # Qué campos mostrar en la LISTA de usuarios
    list_display = ('email', 'nombres', 'apellidos', 'tipo_usuario', 'is_staff', 'is_active')
    
    # Qué campos permitirán hacer búsquedas
    search_fields = ('email', 'nombres', 'apellidos', 'rut_base')
    
    # Qué campos se pueden usar para filtrar
    list_filter = ('tipo_usuario', 'is_active', 'is_staff')
    
    # Qué campo se usará para el login en /admin (es nuestro USERNAME_FIELD)
    ordering = ('email',)
    
    # Campo 'password' no se debe leer
    readonly_fields = ('last_login', 'creado_at')

    # Le decimos al admin que el campo 'username' (que UserAdmin espera)
    # no existe en nuestro modelo.
    filter_horizontal = ()
    
    # Necesario porque sobreescribimos 'fieldsets'
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            # Si un usuario NO es superadmin, no puede editar permisos
            form.base_fields['is_superuser'].disabled = True
        return form

# --- FIN: Configuración del Admin para Usuario ---