from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD, Usuario  # noqa: F401
from db.models.Marcador import MarcadorInsert, MarcadorBD
from settings import CONSULTA_USUARIO, CONSULTA_USUARIO_COMPLETO  # noqa: F401
from settings import (
    CONSULTA_MARCADORES,
    ETIQUETAS_PREDEFINIDAS,
    INSERTAR_ETIQUETA,
    INSERTAR_MARCADOR,
    MARCADORES_PREDETERMINADOS,
    CONSULTA_NUMERO_MARCADORES,
)


def obtener_usuario_completo(email):
    # RecuperciÃ³n de los usuarios como instancias de la clase UsuarioBD
    usuario_completo = gestor_bd.ejecutar_consulta(CONSULTA_USUARIO_COMPLETO, (email,))
    if usuario_completo and isinstance(usuario_completo, list):
        return UsuarioBD(*usuario_completo[0])
    else:
        return []


def crear_marcadores_y_etiquetas_por_defecto(usuario_id):
    marcadores_predeterminados = [
        MarcadorInsert(usuario_id, **marcador)
        for marcador in MARCADORES_PREDETERMINADOS
    ]

    """Inserta marcadores y etiquetas predeterminadas al registrarse."""
    for marcador in marcadores_predeterminados:
        gestor_bd.ejecutar_consulta(
            INSERTAR_MARCADOR,
            (marcador.obtener_info_marcador),
        )

    resultado = gestor_bd.ejecutar_consulta(CONSULTA_MARCADORES, (usuario_id,))
    if resultado and isinstance(resultado, list):
        marcadores = [MarcadorBD(*marcador) for marcador in resultado]
    else:
        marcadores = []

    for marcador, etiqueta in zip(marcadores, ETIQUETAS_PREDEFINIDAS):
        gestor_bd.ejecutar_consulta(
            INSERTAR_ETIQUETA,
            (etiqueta["nombre"], marcador.id),
        )


def obtener_numero_marcadores(usuario_id):
    """Obtiene el número de marcadores de un usuario."""
    resultado = gestor_bd.ejecutar_consulta(CONSULTA_NUMERO_MARCADORES, (usuario_id,))
    if resultado and isinstance(resultado, list):
        return resultado[0][0]  # Retorna el conteo de marcadores
    else:
        return 0
