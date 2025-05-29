#   QUERIES DE USUARIOS

# Script Insertar Usuario
INSERTAR_USUARIO = "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"

# Consultas de Usuario
CONSULTA_USUARIO = "SELECT id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios WHERE email = ? "
BUSCAR_USUARIO = "SELECT * FROM usuarios WHERE id = ?"

# Actualizar Usuario
ACTUALIZAR_USUARIO = " UPDATE usuarios SET nombre_completo = ?, foto_perfil = ?, email = ?, contraseña = ? WHERE id = ? "

# Eliminar Usuario
BORRAR_USUARIO = "DELETE FROM usuarios WHERE id = ?"