# Importamos los módulos base de Django para crear modelos
from django.db import models
# Importamos las clases base para crear un modelo de Usuario personalizado
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# --- INICIO: Administrador de Usuarios ---

class UsuarioManager(BaseUserManager):
    """
    Este es el "Administrador" de nuestro modelo Usuario.
    Le enseña a Django cómo crear usuarios ("create_user")
    y superusuarios ("create_superuser") usando nuestro modelo personalizado.
    """

    def create_user(self, email, rut_base, rut_dv, nombres, apellidos, password=None, **extra_fields):
        """
        Crea y guarda un Usuario regular con el email, RUT, nombres y password.
        """
        # Validación simple: ¡el email es obligatorio!
        if not email:
            raise ValueError('El campo Email es obligatorio')
        
        # Validación simple: ¡el RUT es obligatorio!
        if not rut_base or not rut_dv:
            raise ValueError('El campo RUT es obligatorio')

        # Normaliza el email (lo pone en minúsculas)
        email = self.normalize_email(email)
        
        # Creamos el objeto Usuario en memoria
        # Usamos self.model para referirnos al modelo que este Manager maneja (Usuario)
        usuario = self.model(
            email=email,
            rut_base=rut_base,
            rut_dv=rut_dv,
            nombres=nombres,
            apellidos=apellidos,
            **extra_fields
        )

        # Encriptamos el password
        usuario.set_password(password)
        
        # Guardamos el usuario en la base de datos
        # (usando self._db aseguramos que funcione en la BD correcta)
        usuario.save(using=self._db)
        
        return usuario

    def create_superuser(self, email, rut_base, rut_dv, nombres, apellidos, password, **extra_fields):
        """
        Crea y guarda un Superusuario.
        Un superusuario tiene todos los permisos por defecto.
        """
        
        # Creamos un usuario normal primero, usando el método de arriba
        usuario = self.create_user(
            email=email,
            rut_base=rut_base,
            rut_dv=rut_dv,
            nombres=nombres,
            apellidos=apellidos,
            password=password,
            **extra_fields
        )

        # --- Le damos los poderes de SuperAdmin ---
        # Estos campos vienen de PermissionsMixin
        usuario.is_superuser = True
        # Este campo lo definiremos nosotros en el modelo
        usuario.is_staff = True 
        
        # Aseguramos que el tipo de usuario sea 'super_admin'
        # Este campo lo definiremos nosotros
        usuario.tipo_usuario = 'super_admin'

        # Guardamos los cambios
        usuario.save(using=self._db)
        
        return usuario

# --- FIN: Administrador de Usuarios ---


# --- INICIO: Modelo de Usuario ---

class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    [MAPEO: Tabla 'usuario']
    Este es nuestro modelo de Usuario personalizado.
    Reemplaza al modelo de Usuario por defecto de Django
    y se mapea a nuestra tabla 'usuario' del script SQL.
    
    Hereda de AbstractBaseUser (para manejar la autenticación base)
    y PermissionsMixin (para manejar los permisos de Django).
    """
    
    # ID: Dejamos que Django maneje el 'id' automáticamente.
    # ¡NO AÑADIMOS 'id_usuario = models.AutoField(primary_key=True)'!
    # Este fue el error que causó el problema.

    # Definimos los tipos de usuario basándonos en el ENUM del SQL
    class TipoUsuario(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Administrador'
        ADMIN = 'admin', 'Administrador'
        USUARIO = 'usuario', 'Usuario' # Residente/Copropietario

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.USUARIO,
        db_comment="Rol del usuario en el sistema (ej: admin, usuario)"
    )

    # Campos de RUT (basado en el SQL)
    rut_base = models.IntegerField(
        db_comment="RUT sin dígito verificador"
    )
    rut_dv = models.CharField(
        max_length=1,
        db_comment="Dígito verificador"
    )

    # Campos de Identificación (basado en el SQL)
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    
    email = models.EmailField(
        max_length=120,
        unique=True, # El email DEBE ser único
        db_comment="Email de login"
    )
    
    telefono = models.CharField(max_length=40, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    # Password: (campo 'pass_hash' en el SQL)
    # AbstractBaseUser ya nos da el campo 'password', que maneja el hash.
    # No necesitamos crear 'pass_hash'.

    # --- Campos de Estado y Control de Django ---
    
    # 'activo' del SQL (mapeado a 'is_active')
    # AbstractBaseUser ya nos da este campo 'is_active'.
    is_active = models.BooleanField(
        default=True,
        db_comment="Indica si el usuario puede iniciar sesión"
    )
    
    # Campo 'is_staff' (Requerido por Django Admin)
    # Define si este usuario puede entrar al panel /admin de Django
    is_staff = models.BooleanField(
        default=False,
        db_comment="Indica si el usuario puede acceder al panel de admin"
    )

    # 'creado_at' del SQL (mapeado a 'date_joined')
    creado_at = models.DateTimeField(
        auto_now_add=True, # Se asigna automáticamente al crear
        db_comment="Fecha de creación del registro"
    )
    
    # --- Configuración del Modelo ---

    # Le decimos a Django que use nuestro Manager personalizado
    objects = UsuarioManager()

    # Campo que se usará para el Login
    USERNAME_FIELD = 'email'
    
    # Campos requeridos al crear un usuario por consola (createsuperuser)
    REQUIRED_FIELDS = ['rut_base', 'rut_dv', 'nombres', 'apellidos']

    # --- Métodos del Modelo ---
    
    def __str__(self):
        """Representación en texto del modelo (ej: en el admin de Django)"""
        return f"{self.nombres} {self.apellidos} ({self.email})"

    def get_full_name(self):
        """Método requerido por Django"""
        return f"{self.nombres} {self.apellidos}"

    def get_short_name(self):
        """Método requerido por Django"""
        return self.nombres

    # --- Meta Opciones ---
    
    class Meta:
        # Nombre de la tabla en la Base de Datos
        # ¡IMPORTANTE! Esto le dice a Django que use el nombre de tabla
        # exacto de nuestro script SQL.
        db_table = 'usuario'
        
        # Restricción UNIQUE (basada en el SQL 'uk_usuario_rut')
        constraints = [
            models.UniqueConstraint(
                fields=['rut_base', 'rut_dv'], 
                name='uk_usuario_rut'
            )
        ]
        
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

# --- FIN: Modelo de Usuario ---


# --- INICIO: Modelo UsuarioAdminCondo ---

class UsuarioAdminCondo(models.Model):
    """
    [MAPEO: Tabla 'usuario_admin_condo']
    Esta es la tabla "pivote" o "through" que conecta a un
    Usuario (de tipo 'admin') con los Condominios que administra.
    """
    
    # NOTA ARQUITECTURAL:
    # A diferencia del script SQL , no usamos una Clave Primaria compuesta.
    # Django funciona mejor con una única Clave Primaria (el 'id'
    # que se añade automáticamente).
    # Mantenemos la lógica de 'PRIMARY KEY (id_usuario, id_condominio)'
    # usando 'unique_together' en la Meta.
    
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE, # Si se borra el usuario, se borra el permiso
        db_column='id_usuario'
    )
    
    id_condominio = models.ForeignKey(
        # --- ¡BUENA PRÁCTICA! ---
        # Usamos una "referencia en string" ('core.Condominio')
        # en lugar de importar el modelo Condominio directamente.
        # Esto evita "importaciones circulares", un error común
        # cuando las apps dependen entre sí.
        'core.Condominio',
        on_delete=models.CASCADE, # Si se borra el condominio, se borra el permiso
        db_column='id_condominio'
    )

    def __str__(self):
        # Usamos 'self.id_usuario' y 'self.id_condominio' que son los
        # objetos FK, para poder acceder a sus nombres.
        try:
            # Intentamos acceder a los objetos relacionados
            # (pueden no existir si algo está mal configurado)
            return f"{self.id_usuario.email} administra {self.id_condominio.nombre}"
        except Exception:
            # Fallback por si los objetos no se pueden cargar
            return f"Relación Admin-Condominio ID: {self.id}"


    class Meta:
        db_table = 'usuario_admin_condo'
        
        # Esto implementa la lógica de la PRIMARY KEY compuesta del SQL 
        # Asegura que no se pueda asignar el mismo usuario al mismo
        # condominio más de una vez.
        unique_together = ('id_usuario', 'id_condominio')
        
        verbose_name = 'Admin por Condominio'
        verbose_name_plural = 'Admins por Condominio'

# --- FIN: Modelo UsuarioAdminCondo ---