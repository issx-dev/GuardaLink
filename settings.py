# LIBRERÍAS
from decouple import config, UndefinedValueError
from modules.utils import info_logs

# VARIABLES DE ENTORNO
try:
    DATABASE_NAME = config("DB_NAME", cast=str)
    ROOT_NAME = config("ROOT_NAME", cast=str)
    ROOT_PASSWORD = config("ROOT_PASSWORD", cast=str)
    ROOT_EMAIL = config("ROOT_EMAIL", cast=str)
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
INSERTAR_USUARIO = (
    "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"  # noqa
)


CONSULTA_USUARIO = "SELECT id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios "
