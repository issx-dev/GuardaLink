# LIBRARIES
from decouple import config, UndefinedValueError
from modules.utils import info_logs

# ENV VARIABLES
try:
    DATABASE_NAME = config("DB_NAME", cast=str)
except UndefinedValueError as e:
    raise UndefinedValueError(
        f"No se ha definido la variable de entorno DB_NAME Detalles: {e} "
    )

info_logs("La variable de entorno DB_NAME se ha definido correctamente.")


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
INSERTAR_USUARIO = "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"  # noqa


CONSULTA_USUARIO = "SELECT id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios "
