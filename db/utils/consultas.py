from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD, Usuario  # noqa: F401
from settings import CONSULTA_USUARIO, CONSULTA_USUARIO_COMPLETO  # noqa: F401


def obtener_usuario_completo(email):
    # Recuperción de los usuarios como instancias de la clase UsuarioBD
    usuario_completo = gestor_bd.ejecutar_consulta(
        CONSULTA_USUARIO_COMPLETO, (email,)
    )
    if usuario_completo and isinstance(usuario_completo, list):
        return UsuarioBD(*usuario_completo[0])
    else:
        return []
