#   QUERIES DE USUARIOS

# Script Insertar Usuario
INSERTAR_USUARIO = "INSERT INTO usuarios (nombre_completo, contraseña, email) VALUES (?, ?, ?)"

# Consultas de Usuario
CONSULTA_USUARIOS = "SELECT * FROM usuarios"
CONSULTA_USUARIO_COMPLETO = "SELECT * FROM usuarios WHERE email = ? "
BUSCAR_USUARIO = "SELECT * FROM usuarios WHERE id = ?"

# Actualizar Usuario
ACTUALIZAR_USUARIO = " UPDATE usuarios SET nombre_completo = ?, foto_perfil = ?, email = ?, contraseña = ? WHERE id = ? "

# Modificar Estado de Usuario
MODIFICAR_ESTADO_USUARIO = "UPDATE usuarios SET estado = ? WHERE id = ?"

# Actualizar Rol de Usuario
ACTUALIZAR_ROL_USUARIO = "UPDATE usuarios SET rol = ? WHERE id = ?"

# Eliminar Usuario
BORRAR_USUARIO = "DELETE FROM usuarios WHERE id = ?"
