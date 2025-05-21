# LIBRERÍAS
from decouple import config, UndefinedValueError
from modules.utils import info_logs
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
    raise UndefinedValueError(
        f"Error al cargar las variables de entorno. Detalles: {e} "
    )

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

INSERTAR_USUARIO = (
    "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"
)


CONSULTA_USUARIO = "SELECT id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios WHERE email = ? "
