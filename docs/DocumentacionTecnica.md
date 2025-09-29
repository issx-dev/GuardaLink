## Arquitectura Interna

### Estructura de Módulos

#### Aplicación Principal (`app.py`)
Punto de entrada de la aplicación que:
- Inicializa la aplicación Flask
- Registra los blueprints
- Maneja rutas principales y errores
- Gestiona la sesión de usuario

#### Blueprints (`blueprints/`)
Módulos organizados por funcionalidad:
- **`usuarios.py`**: Autenticación, registro, perfil y gestión de usuarios
- **`marcadores.py`**: CRUD completo de marcadores
- **`buscador.py`**: Funcionalidades de búsqueda y filtrado

#### Base de Datos (`db/`)
Gestión completa de la base de datos:
- **`BaseDatos.py`**: Clase principal para conexión y consultas SQLite
- **`models/`**: Modelos de datos (Usuario, Marcador, Etiqueta)
- **`queries/`**: Consultas SQL organizadas por entidad
- **`utils/`**: Utilidades y funciones auxiliares para BD

#### Utilidades (`modules/`)
Funciones auxiliares del sistema:
- **`utils.py`**: Funciones de logging, sesión y utilidades generales

## Configuración y Conexión con SQLite

### Variables de Entorno (.env)
El sistema requiere las siguientes variables de configuración:

```bash
# Configuración de Base de Datos
DB_NAME=guardaLink.db

# Seguridad
SECRET_KEY=clave-secreta

# Usuario Administrador por Defecto
ROOT_NAME=Administrador
ROOT_PASSWORD=admin123
ROOT_EMAIL=admin@guardalink.com
ROOT_FOTO=https://example.com/avatar.jpg
```

### Esquema de Base de Datos

#### Tabla `usuarios`
```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT "usuario",
    email TEXT NOT NULL UNIQUE,
    estado INTEGER NOT NULL DEFAULT 1,
    foto_perfil TEXT DEFAULT "https://thumb.ac-illust.com/51/51e1c1fc6f50743937e62fca9b942694_t.jpeg",
    fecha_registro DATE DEFAULT CURRENT_DATE
);
```

#### Tabla `marcadores`
```sql
CREATE TABLE IF NOT EXISTS marcadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    enlace TEXT NOT NULL,
    descripcion TEXT DEFAULT "Descripción del marcador",
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

#### Tabla `etiquetas`
```sql
CREATE TABLE IF NOT EXISTS etiquetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL COLLATE NOCASE,
    id_marcador INTEGER NOT NULL,
    FOREIGN KEY (id_marcador) REFERENCES marcadores(id) ON DELETE CASCADE,
    UNIQUE(nombre, id_marcador)
);
```

### Configuración de Conexión

```python
class BaseDeDatos:
    def __init__(self):
        self._inicializar_base()

    def _inicializar_base(self):
        try:
            with sq.connect(DATABASE_NAME) as conexion:
                cursor = conexion.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.executescript(CREAR_TABLAS)
                cursor.execute(CREAR_ROOT, INFO_ROOT)
                conexion.commit()
                info_logs(" -> Conexión establecida correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al conectar con la base de datos: {e}")
            raise
```

## Endpoints

### Rutas de Usuarios (`/usuarios`)

| Ruta | Método | Parámetros | Respuesta | Descripción |
|------|--------|------------|-----------|-------------|
| `/acceso` | GET | - | HTML | Página de login y registro |
| `/acceso` | POST | `nombre-completo`, `email`, `contraseña` | Redirect | Procesa registro/login |
| `/perfil` | GET | - | HTML | Página de perfil del usuario |
| `/perfil` | POST | `nombre-completo`, `foto-perfil`, `email`, `contraseña` | Redirect | Actualiza perfil |
| `/mod-cuenta/<accion>/<id_usuario>` | GET | `accion`, `id_usuario` | Redirect | Gestión de cuentas (admin) |

### Rutas de Marcadores (`/marcador`)

| Ruta | Método | Parámetros | Respuesta | Descripción |
|------|--------|------------|-----------|-------------|
| `/` | GET | - | HTML | Formulario nuevo marcador |
| `/añadir` | POST | `nombre`, `enlace`, `descripcion`, `etiquetas` | Redirect | Crea nuevo marcador |
| `/editar/<id_marcador>` | GET | `id_marcador` | HTML | Formulario edición |
| `/editar/<id_marcador>` | POST | `nombre`, `enlace`, `descripcion`, `etiquetas` | Redirect | Actualiza marcador |
| `/eliminar/<id_marcador>` | GET | `id_marcador` | Redirect | Elimina marcador |

### Rutas de Búsqueda (`/buscador`)

| Ruta | Método | Parámetros | Respuesta | Descripción |
|------|--------|------------|-----------|-------------|
| `/` | POST | `buscador_marcadores` | HTML | Búsqueda general |
| `/<filtro_etiqueta>` | GET | `filtro_etiqueta` | HTML | Filtro por etiqueta |

### Rutas Principales

| Ruta | Método | Parámetros | Respuesta | Descripción |
|------|--------|------------|-----------|-------------|
| `/` | GET | - | HTML | Página principal |
| `/cerrar-sesion` | GET | - | Redirect | Cierra sesión del usuario |

## Fragmentos de Código de Ejemplo

### Gestión de Sesión

```python
def usr_sesion():
    """Obtiene el usuario de la sesión actual"""
    email_sesion = session.get("email")
    if email_sesion:
        return obtener_usuario_completo(email_sesion)
    return None
```

### CRUD de Marcadores

```python
@marcador_bp.route("/añadir", methods=["POST"])
def añadir_marcador():
    # Convertimos los datos del formulario en una lista para separar las etiquetas
    datos = list(request.form.values())
    # Obtenemos las etiquetas
    etiquetas = datos.pop(-1).strip()
    # Eliminamos espacios y capitalizamos las etiquetas
    etiquetas = [
        etiqueta.strip().capitalize()
        for etiqueta in etiquetas.split(",")
        if etiqueta.strip()
    ]
    
    # Crea el objeto marcador
    marcador = MarcadorInsert(usuario.id, *datos)
    
    # Sube el marcador a la bd
    marcador_id = gestor_bd.ejecutar_consulta(
        INSERTAR_MARCADOR,
        (marcador.obtener_info_marcador),
        retornar_id=True,
    )
```

### Modelo de Usuario
```python
class UsuarioBD(UsuarioInsert):
    def __init__(
        self,
        id: int,
        nombre_completo: str,
        contraseña: str,
        rol: str,
        email: str,
        estado: bool,
        foto_perfil: str,
        fecha_registro: str,
    ):
        super().__init__(nombre_completo, contraseña, email)
        self.__id = id
        self.__rol = rol
        self.__estado = estado
        self.__foto_perfil = foto_perfil
        self.__fecha_registro = fecha_registro
```

### Consulta con JOINs

```python 
CONSULTAR_MARCADORES_ETIQUETAS = """
    SELECT  
        m.id, m.id_usuario, m.nombre, m.enlace, m.descripcion,
        GROUP_CONCAT(e.nombre, ',') AS etiquetas
    FROM marcadores m 
    JOIN etiquetas e ON m.id = e.id_marcador 
    WHERE m.id_usuario = ?
    GROUP BY m.id
"""
```

### Hash de Contraseñas

```python 
# Registro de usuario con hash de contraseña
usr = UsuarioInsert(nombre_completo, pbkdf2_sha256.hash(contraseña), email)
gestor_bd.ejecutar_consulta(
    INSERTAR_USUARIO,
    usr.obtener_datos,
)

# Verificación de contraseña en login
if isinstance(usuario_actual, UsuarioBD) and pbkdf2_sha256.verify(
    contraseña,
    usuario_actual.contraseña,
):
    # Login exitoso
    session["email"] = email
    return redirect(url_for("index"))
```

## Notas Técnicas

### Gestión de Estados
- **Usuarios activos/inactivos**: Control de acceso mediante campo `estado`
- **Roles diferenciados**: Los administradores no pueden crear marcadores
- **Sesiones persistentes**: Mantenimiento de estado entre peticiones

### Manejo de Errores
```python 
except sq.Error as e:
    error_logs(
        f" !-> Error al ejecutar la consulta de base de datos. DETALLES: {e}"
    )
    return False
```

### Logging del Sistema
```python 
def info_logs(mensaje):
    """Registra mensajes informativos"""
    print(f"[INFO] {mensaje}")

def error_logs(mensaje):
    """Registra mensajes de error"""
    print(f"[ERROR] {mensaje}")
```

## Referencias

### Documentación Técnica Externa
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Passlib Documentation](https://passlib.readthedocs.io/)

### Archivos de Configuración Importantes
- `settings.py` - Configuración principal y variables de entorno
- `requirements.txt` - Dependencias del proyecto
- `.env.example` - Ejemplo de variables de entorno
- `app.py` - Punto de entrada de la aplicación