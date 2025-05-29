# Librerías necesarias
from flask import Blueprint, request, session, render_template, redirect, url_for, flash

# Modulos necesarios
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD
from db.queries.etiquetas import ETIQUETAS_MAS_USADAS
from db.queries.marcadores import BUSCADOR_MARCADORES, FILTRAR_MARCADORES_POR_ETIQUETAS
from db.utils.consultas import obtener_marcadores_especificos, obtener_usuario_completo

# Inicializa el blueprint para marcadores
buscador_bp = Blueprint("buscador", __name__, url_prefix="/buscador")


# Buscador marcadores
@buscador_bp.route("/<filtro_etiqueta>")
@buscador_bp.route("/", methods=["GET", "POST"])
def buscar_marcador(filtro_etiqueta=None):
    """Obtiene el usuario logueado y su rol"""
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("usuarios.acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        flash("Los administradores no tienen acceso al buscador.", "error")
        return redirect(url_for("index"))

    etiquetas_mas_usadas = gestor_bd.ejecutar_consulta(
        ETIQUETAS_MAS_USADAS, (usuario.id,)
    )

    if filtro_etiqueta:
        resultado = gestor_bd.ejecutar_consulta(
            FILTRAR_MARCADORES_POR_ETIQUETAS, (usuario.id, f"%{filtro_etiqueta}%")
        )

        lista_IDs = []
        if isinstance(resultado, list):
            lista_IDs = [marcador[0] for marcador in resultado]
        else:
            flash(
                "No se ha encotrado ningún resultado que coincida con las búsqueda.",
                "info",
            )

        # Marcadores de la búsqueda
        marcadores = obtener_marcadores_especificos(usuario.id, lista_IDs)

        return render_template(
            "index.html",
            marcadores=marcadores,
            foto_perfil=usuario.foto_perfil,
            etiquetas_mas_usadas=etiquetas_mas_usadas,
        )

    # Busqueda de marcadores
    busqueda = request.form.get("buscador_marcadores", "").strip()
    # Formateo busqueda para SQL
    busqueda = f"%{busqueda}%"
    # Ejecutamos la consulta para buscar marcadores
    resultado = gestor_bd.ejecutar_consulta(
        BUSCADOR_MARCADORES, (usuario.id, busqueda, busqueda, busqueda)
    )

    lista_IDs = []
    if isinstance(resultado, list):
        lista_IDs = [marcador[0] for marcador in resultado]
    else:
        flash(
            "No se ha encotrado ningún resultado que coincida con las búsqueda.", "info"
        )

    # Marcadores de la búsqueda
    marcadores = obtener_marcadores_especificos(usuario.id, lista_IDs)

    return render_template(
        "index.html",
        marcadores=marcadores,
        foto_perfil=usuario.foto_perfil,
        etiquetas_mas_usadas=etiquetas_mas_usadas,
    )
