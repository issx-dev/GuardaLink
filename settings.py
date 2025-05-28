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
    FOREIGN KEY (id_marcador) REFERENCES marcadores(id) ON DELETE CASCADE,
    UNIQUE(nombre, id_marcador) -- Evita etiquetas duplicadas para el mismo marcador
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

# Actualizar Usuario
ACTUALIZAR_USUARIO = " UPDATE usuarios SET nombre_completo = ?, foto_perfil = ?, email = ?, contraseña = ? WHERE id = ? "

# Script Insertar Marcador y Consulta
INSERTAR_MARCADOR = "INSERT INTO marcadores (id_usuario, nombre, enlace, descripcion) VALUES (?, ?, ?, ?)"
CONSULTA_MARCADOR = "SELECT * FROM marcadores WHERE id = ?"
CONSULTA_MARCADORES = "SELECT * FROM marcadores WHERE id_usuario = ?"
CONSULTA_NUMERO_MARCADORES = "SELECT COUNT(*) FROM marcadores WHERE id_usuario = ?"

ACTUALIZAR_MARCADOR = """
UPDATE marcadores
SET nombre = ?, enlace = ?, descripcion = ?
WHERE id = ? 
"""

CONSULTAR_MARCADORES_ETIQUETAS = """
            SELECT  
                m.id, m.id_usuario, m.nombre, m.enlace, m.descripcion,
                GROUP_CONCAT(e.nombre, ',') AS etiquetas
            FROM marcadores m 
            JOIN etiquetas e ON m.id = e.id_marcador 
            WHERE m.id_usuario = ?
            GROUP BY m.id
"""

# Script Insertar Etiqueta y Consulta
INSERTAR_ETIQUETA = "INSERT OR IGNORE INTO etiquetas (nombre, id_marcador) VALUES (?, ?)"
CONSULTA_ETIQUETAS = "SELECT * FROM etiquetas WHERE id_marcador = ?"
CONSULTA_NOMBRES_ETIQUETAS = "SELECT nombre FROM etiquetas WHERE id_marcador = ?"

# MARCADORES PREDETERMINADOS
MARCADORES_PREDETERMINADOS = [
    {
        "nombre": "Google",
        "enlace": "https://www.google.com",
        "descripcion": "El buscador más utilizado del mundo.",
        "etiquetas": ["Tecnología", "Buscador"],
    },
    {
        "nombre": "Wikipedia",
        "enlace": "https://www.wikipedia.org",
        "descripcion": "La enciclopedia libre y colaborativa.",
        "etiquetas": ["Educación", "Referencia"],
    },
    {
        "nombre": "GitHub",
        "enlace": "https://github.com",
        "descripcion": "Plataforma de desarrollo colaborativo de software.",
        "etiquetas": ["Tecnología", "Desarrollo"],
    },
]

# BÚSQUEDAS
BUSCADOR_MARCADORES = """
SELECT * FROM marcadores 
    WHERE id_usuario = ? AND (LOWER(nombre) LIKE ? OR LOWER(descripcion) LIKE ? OR LOWER(enlace) LIKE ?)
    ORDER BY id ASC
"""

# ETIQUETAS MÁS USADAS
ETIQUETAS_MAS_USADAS = """
SELECT e.nombre
FROM marcadores m
JOIN etiquetas e ON m.id = e.id_marcador
WHERE m.id_usuario = ?
GROUP BY e.nombre
ORDER BY COUNT(*) DESC LIMIT 5
"""

# BUSCAR MARCADORES POR ETIQUERAS
FILTRAR_MARCADORES_POR_ETIQUETAS = """
SELECT m.id, m.id_usuario, m.nombre, m.enlace, m.descripcion, GROUP_CONCAT(e.nombre, ',') AS etiquetas
FROM marcadores m
JOIN etiquetas e ON m.id = e.id_marcador
WHERE m.id_usuario = ? 
AND e.nombre LIKE ?
GROUP BY m.id
"""


