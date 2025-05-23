# LIBRERÍAS
from decouple import config, UndefinedValueError
from modules.utils import info_logs, error_logs
from passlib.hash import pbkdf2_sha256

# VARIABLES DE ENTORNO
try:
    DATABASE_NAME = str(config("DB_NAME"))
    SECRET_KEY = str(config("SECRET_KEY"))
    ROOT_NAME = str(config("ROOT_NAME"))
    ROOT_PASSWORD = str(config("ROOT_PASSWORD"))
    ROOT_EMAIL = str(config("ROOT_EMAIL"))
    ROOT_FOTO = str(config("ROOT_FOTO"))
except UndefinedValueError as e:
    error_logs(f"Error al cargar las variables de entorno. Detalles: {e} ")
    raise UndefinedValueError

info_logs("La variables de entorno se han cargado correctamente.")


CREAR_TABLAS = """ 
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

CREATE TABLE IF NOT EXISTS marcadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    enlace TEXT NOT NULL,
    descripcion TEXT DEFAULT "Descripción del marcador",
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS etiquetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    id_marcador INTEGER NOT NULL,
    FOREIGN KEY (id_marcador) REFERENCES marcadores(id) ON DELETE CASCADE
);
"""

CREAR_ROOT = "INSERT OR IGNORE INTO usuarios (nombre_completo, contraseña, rol, email, foto_perfil) VALUES (?, ?, ?, ?, ?);"
# Carga de la información del root y cifrado de la contraseña
INFO_ROOT = (
    ROOT_NAME,
    pbkdf2_sha256.hash(ROOT_PASSWORD),
    "admin",
    ROOT_EMAIL,
    ROOT_FOTO,
)

# Script Insertar Usuario
INSERTAR_USUARIO = (
    "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"
)

# Consultas de Usuario
CONSULTA_USUARIO = "SELECT id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios WHERE email = ? "

# Script Insertar Marcador y Consulta
INSERTAR_MARCADOR = "INSERT INTO marcadores (id_usuario, nombre, enlace, descripcion) VALUES (?, ?, ?, ?)"
CONSULTA_MARCADORES = "SELECT * FROM marcadores WHERE id_usuario = ?"
CONSULTA_NUMERO_MARCADORES = "SELECT COUNT(*) FROM marcadores WHERE id_usuario = ?"

# Script Insertar Etiqueta y Consulta
INSERTAR_ETIQUETA = "INSERT INTO etiquetas (nombre, id_marcador) VALUES (?, ?)"
CONSULTA_ETIQUETAS = "SELECT * FROM etiquetas WHERE id_marcador = ?"

# MARCADORES PREDETERMINADOS
MARCADORES_PREDETERMINADOS = [
    {
        "nombre": "Google",
        "enlace": "https://www.google.com",
        "descripcion": "El buscador más utilizado del mundo.",
    },
    {
        "nombre": "Wikipedia",
        "enlace": "https://www.wikipedia.org",
        "descripcion": "La enciclopedia libre y colaborativa.",
    },
    {
        "nombre": "GitHub",
        "enlace": "https://github.com",
        "descripcion": "Plataforma de desarrollo colaborativo de software.",
    },
]
# Etiquetas predefinidas para los marcadores
ETIQUETAS_PREDEFINIDAS = [
    {"nombre": "Tecnología"},
    {"nombre": "Educación"},
    {"nombre": "Desarrollo"},
]