# from db.BaseDatos import gestor_bd
# from db.models.Usuario import UsuarioInsert, UsuarioBD, Usuario
# from settings import INSERTAR_USUARIO, CONSULTA_USUARIO, CONSULTA_USUARIO_COMPLETO

# Ejemplo de inserción de usuario
# usr = UsuarioInsert("gussi", "1368146", "ratita@colita.com")
# gestor_bd.ejecutar_consulta(
#     INSERTAR_USUARIO,
#     usr.obtener_datos,
# )

# Recuperción de los usuarios como instancias de la clase Usuario
# consulta_resultado = gestor_bd.ejecutar_consulta(CONSULTA_USUARIO)
# if isinstance(consulta_resultado, list):
#     usuarios = [Usuario(*usr) for usr in consulta_resultado]
# else:
#     usuarios = []

# # Recuperción de los usuarios como instancias de la clase UsuarioBD
# consulta_completa_resultado = gestor_bd.ejecutar_consulta(CONSULTA_USUARIO_COMPLETO)
# if isinstance(consulta_completa_resultado, list):
#     usuarios_completos = [UsuarioBD(*usr) for usr in consulta_completa_resultado]
# else:
#     usuarios_completos = []
