# Librerías necesarias
from flask import Blueprint, request, render_template, redirect, url_for, flash

# Módulos necesarios
from db.BaseDatos import gestor_bd
from db.models.Marcador import MarcadorInsert, MarcadorBD
from db.models.Usuario import UsuarioBD
from db.models.Etiqueta import EtiquetaInsert
from db.queries.etiquetas import (
    BORRAR_ETIQUETA,
    CONSULTA_NOMBRES_ETIQUETAS,
    INSERTAR_ETIQUETA,
)
from db.queries.marcadores import (
    ACTUALIZAR_MARCADOR,
    CONSULTA_MARCADOR,
    ELIMINAR_MARCADOR,
    INSERTAR_MARCADOR,
)
from modules.utils import usr_sesion

# Inicializa el blueprint para marcadores
marcador_bp = Blueprint("marcadores", __name__, url_prefix="/marcador")


@marcador_bp.route("/<accion>/<id_marcador>", methods=["GET", "POST"])
@marcador_bp.route("/<accion>", methods=["GET", "POST"])
@marcador_bp.route("/")
def marcador(accion=None, id_marcador=None):
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("usuarios.acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        flash("Los administradores no pueden gestionar marcadores.", "error")
        return redirect(url_for("index"))

    # Si el usuario logueado es NORMAL
    # Acciones de marcador
    match accion:
        case "editar":
            marcador = gestor_bd.ejecutar_consulta(
                CONSULTA_MARCADOR,
                (id_marcador,),
            )

            if isinstance(marcador, list) and marcador:
                marcador = MarcadorBD(*marcador[0])
            else:
                flash("Marcador no encontrado.", "error")
                return redirect(url_for("index"))

            if not isinstance(marcador, MarcadorBD):
                flash("Marcador no encontrado.", "error")
                return redirect(url_for("index"))

            # Obtenemos las etiquetas del marcador
            etiquetas = gestor_bd.ejecutar_consulta(
                CONSULTA_NOMBRES_ETIQUETAS, (id_marcador,)
            )

            if request.method == "POST":
                # Si el usuario logueado es NORMAL obtenemos los datos del formulario
                nombre = request.form.get("nombre", "").strip()
                enlace = request.form.get("enlace", "").strip()
                descripcion = request.form.get("descripcion", "").strip()
                etiquetas_nuevas = request.form.get("etiquetas", "").strip().split(",")

                # Si no se han realizado cambios en el perfil mandamos un mensaje
                # y redirigimos al perfil
                if not nombre and not enlace and not descripcion and not etiquetas:
                    flash("No se han realizado cambios en el marcador.", "info")
                    return redirect(url_for("index"))

                # Validación de los campos para actualizar solo los que se han modificado
                nombre = nombre or marcador.nombre
                enlace = enlace or marcador.enlace
                descripcion = descripcion or marcador.descripcion
                etiquetas = etiquetas_nuevas or etiquetas

                # Actualizamos el marcador
                gestor_bd.ejecutar_consulta(
                    ACTUALIZAR_MARCADOR,
                    (
                        nombre,
                        enlace,
                        descripcion,
                        id_marcador,
                    ),
                )

                # Borrar etiquetas antiguas
                gestor_bd.ejecutar_consulta(BORRAR_ETIQUETA, (id_marcador,))

                # Insertar nuevas etiquetas
                for etiqueta in etiquetas:  # type: ignore
                    gestor_bd.ejecutar_consulta(
                        INSERTAR_ETIQUETA, (etiqueta.strip(), id_marcador)
                    )

                # Mensaje de éxito
                flash("Marcador actualizado correctamente.", "success")
                return redirect(url_for("index"))

            etiquetas_str = ", ".join([etiqueta[0] for etiqueta in etiquetas])  # type: ignore

            return render_template(
                "marcador.html",
                foto_perfil=usuario.foto_perfil,
                editar=True,
                marcador=marcador,
                etiquetas=etiquetas_str,
            )

        case "eliminar":
            gestor_bd.ejecutar_consulta(ELIMINAR_MARCADOR, (id_marcador,))
            flash("Marcador eliminado correctamente.", "success")

            return redirect(url_for("index"))

        case "añadir":
            if request.method == "POST":
                # Convertimos los datos del formulario en una lista para separar las etiquetas
                datos = list(request.form.values())
                # Obtenemos las etiquetas
                etiquetas = datos.pop(-1).strip()
                # Eliminamos espacios y capitalizamos las etiquetas
                etiquetas = [
                    etiqueta.strip().capitalize()
                    for etiqueta in etiquetas.split(",")
                    if etiqueta.strip()
                ]

                # Crea el objeto marcador
                marcador = MarcadorInsert(usuario.id, *datos)

                # Sube el marcador a la bd
                marcador_id = gestor_bd.ejecutar_consulta(
                    INSERTAR_MARCADOR,
                    (marcador.obtener_info_marcador),
                    retornar_id=True,
                )

                # Si no se ha insertado el marcador, mostramos un mensaje de error
                if not marcador_id:
                    flash("Error al añadir el marcador.", "error")
                    return redirect(url_for("marcadores.marcador"))

                # Insertar las etiquetas del marcador
                for etiqueta in etiquetas:
                    gestor_bd.ejecutar_consulta(
                        INSERTAR_ETIQUETA,
                        (EtiquetaInsert(etiqueta, marcador_id).obtener_datos),
                    )

                # Mensaje de éxito y redirección
                flash("Marcador añadido correctamente.", "success")

                return redirect(url_for("index"))

    return render_template("marcador.html", foto_perfil=usuario.foto_perfil)
