#   QUERIES DE ETIQUETAS

# Script Insertar Etiqueta
INSERTAR_ETIQUETA = "INSERT OR IGNORE INTO etiquetas (nombre, id_marcador) VALUES (?, ?)"

# Consultas de Etiquetas
CONSULTA_ETIQUETAS = "SELECT * FROM etiquetas WHERE id_marcador = ?"
CONSULTA_NOMBRES_ETIQUETAS = "SELECT nombre FROM etiquetas WHERE id_marcador = ?"
ETIQUETAS_MAS_USADAS = """
SELECT e.nombre
FROM marcadores m
JOIN etiquetas e ON m.id = e.id_marcador
WHERE m.id_usuario = ?
GROUP BY e.nombre
ORDER BY COUNT(*) DESC LIMIT 5
"""

# Borrar Etiqueta
BORRAR_ETIQUETA = "DELETE FROM etiquetas WHERE id_marcador = ?"
