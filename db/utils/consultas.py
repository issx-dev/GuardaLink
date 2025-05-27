from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD
from db.models.Marcador import MarcadorBD
from settings import (
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
    """Inserta marcadores y etiquetas predeterminadas para un usuario."""
    # Insertar todos los marcadores primero
    for marcador in MARCADORES_PREDETERMINADOS:
        # Insertar marcador
        marcador_id = gestor_bd.ejecutar_consulta(
            INSERTAR_MARCADOR,
            (
                usuario_id,
                marcador["nombre"],
                marcador["enlace"],
                marcador["descripcion"],
            ),
            retornar_id=True,
        )

        # Extraer el ID del resultado de la consulta
        if not marcador_id:
            raise ValueError("Error al obtener ID del marcador insertado")

        # Insertar etiquetas asociadas
        for etiqueta in marcador["etiquetas"]:
            gestor_bd.ejecutar_consulta(INSERTAR_ETIQUETA, (etiqueta, marcador_id))


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


def obtener_marcadores_especificos(usuario_id, lista_marcadores):
    lista = []
    for marcador in obtener_marcadores_y_etiquetas(usuario_id):
        if marcador[0].id in lista_marcadores:
            lista.append(marcador)

    return lista


def obtener_numero_marcadores(usuario_id):
    """Obtiene el número de marcadores de un usuario."""
    resultado = gestor_bd.ejecutar_consulta(CONSULTA_NUMERO_MARCADORES, (usuario_id,))
    if resultado and isinstance(resultado, list):
        return resultado[0][0]  # Retorna el conteo de marcadores
    else:
        return 0
