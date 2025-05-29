#   QUERIES DE MARCADORES

# Script Insertar Marcador
INSERTAR_MARCADOR = "INSERT INTO marcadores (id_usuario, nombre, enlace, descripcion) VALUES (?, ?, ?, ?)"

# Consultas de Marcadores
CONSULTA_MARCADOR = "SELECT * FROM marcadores WHERE id = ?"
CONSULTA_MARCADORES = "SELECT * FROM marcadores WHERE id_usuario = ?"
CONSULTA_NUMERO_MARCADORES = "SELECT COUNT(*) FROM marcadores WHERE id_usuario = ?"
CONSULTAR_MARCADORES_ETIQUETAS = """
            SELECT  
                m.id, m.id_usuario, m.nombre, m.enlace, m.descripcion,
                GROUP_CONCAT(e.nombre, ',') AS etiquetas
            FROM marcadores m 
            JOIN etiquetas e ON m.id = e.id_marcador 
            WHERE m.id_usuario = ?
            GROUP BY m.id
"""

# Actualizar Marcador
ACTUALIZAR_MARCADOR = """
UPDATE marcadores
SET nombre = ?, enlace = ?, descripcion = ?
WHERE id = ? 
"""

# Eliminar Marcador
ELIMINAR_MARCADOR = "DELETE FROM marcadores WHERE id = ?"

# Busquedas de Marcadores
BUSCADOR_MARCADORES = """
SELECT * FROM marcadores 
    WHERE id_usuario = ? AND (LOWER(nombre) LIKE ? OR LOWER(descripcion) LIKE ? OR LOWER(enlace) LIKE ?)
    ORDER BY id ASC
"""
FILTRAR_MARCADORES_POR_ETIQUETAS = """
SELECT m.id, m.id_usuario, m.nombre, m.enlace, m.descripcion, GROUP_CONCAT(e.nombre, ',') AS etiquetas
FROM marcadores m
JOIN etiquetas e ON m.id = e.id_marcador
WHERE m.id_usuario = ? 
AND e.nombre LIKE ?
GROUP BY m.id
"""
