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