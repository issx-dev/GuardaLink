from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD
from db.models.Marcador import MarcadorInsert, MarcadorBD
from settings import (
    CONSULTA_MARCADORES,
    ETIQUETAS_PREDEFINIDAS,
    INSERTAR_ETIQUETA,
    INSERTAR_MARCADOR,
    MARCADORES_PREDETERMINADOS,
    CONSULTA_NUMERO_MARCADORES,
    CONSULTA_USUARIO_COMPLETO,
    CONSULTAR_MARCADORES_ETIQUETAS,
)


def obtener_usuario_completo(email):
    # Recupercion de los usuarios como instancias de la clase UsuarioBD
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


def obtener_marcadores_y_etiquetas(usuario_id):
    """Obtiene los marcadores de un usuario."""
    resultado = gestor_bd.ejecutar_consulta(
        CONSULTAR_MARCADORES_ETIQUETAS, (usuario_id,)
    )
    if isinstance(resultado, list):
        return [
            (MarcadorBD(*marcador[:-1]), marcador[-1].split(","))
            for marcador in resultado
        ]
    else:
        return []


def obtener_numero_marcadores(usuario_id):
    """Obtiene el número de marcadores de un usuario."""
    resultado = gestor_bd.ejecutar_consulta(CONSULTA_NUMERO_MARCADORES, (usuario_id,))
    if resultado and isinstance(resultado, list):
        return resultado[0][0]  # Retorna el conteo de marcadores
    else:
        return 0
