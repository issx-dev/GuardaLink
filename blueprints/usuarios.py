# Librerías necesarias
from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256

# Configuración y consultas necesarias
from db.queries.usuarios import (
    ACTUALIZAR_USUARIO,
    BORRAR_USUARIO,
    INSERTAR_USUARIO,
    MODIFICAR_ESTADO_USUARIO,
)
from db.utils.consultas import (
    obtener_usuario_completo,
    crear_marcadores_y_etiquetas_por_defecto,
    obtener_numero_marcadores,
    obtener_usuario_por_id,
)
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioInsert, UsuarioBD
from modules.utils import usr_sesion

# Inicializa el blueprint para usuarios
usuario_bp = Blueprint("usuarios", __name__)


# CRUD DE USUARIOS
# Inicio de sesión y registro de nuevos usuarios
@usuario_bp.route("/acceso", methods=["GET", "POST"])
def acceso():
    """Permite a los usuarios iniciar sesión o registrarse."""

    if request.method == "POST":
        # Obtiene los datos del formulario html
        nombre_completo = request.form.get("nombre-completo", "").strip()
        email = request.form.get("email", "").strip().lower()
        contraseña = request.form.get("contraseña", "")

        if not email or not contraseña:
            flash("Por favor, rellena todos los campos obligatorios.", "error")
            return redirect(url_for("usuarios.acceso"))

        # Obtiene la instancia usuario de la sesión actual
        usuario_actual = obtener_usuario_completo(email)

        # Registro
        if "registrarse" in request.form:
            if isinstance(usuario_actual, UsuarioBD):
                flash(
                    "Este email ya está registrado, por favor Inicie Sesión.", "error"
                )
                return redirect(url_for("usuarios.acceso"))

            # Inserción de usuario en la BD
            usr = UsuarioInsert(nombre_completo, pbkdf2_sha256.hash(contraseña), email)
            gestor_bd.ejecutar_consulta(
                INSERTAR_USUARIO,
                usr.obtener_datos,
            )

            usuario_actual = obtener_usuario_completo(email)
            if not isinstance(usuario_actual, UsuarioBD):
                flash(
                    "Error al registrar el usuario, por favor inténtelo de nuevo.",
                    "error",
                )
                gestor_bd._inicializar_base()
                return redirect(url_for("usuarios.acceso"))
            crear_marcadores_y_etiquetas_por_defecto(usuario_actual.id)

            session["email"] = email
            return redirect(url_for("index"))

        # Inicio de sesión
        elif "iniciar-sesion" in request.form:
            if isinstance(usuario_actual, UsuarioBD) and pbkdf2_sha256.verify(
                contraseña,
                usuario_actual.contraseña,
            ):
                if not usuario_actual.estado:
                    flash(
                        "Tu cuenta ha sido desactivada. Por favor, contacta con el administrador.",
                        "error",
                    )
                    return redirect(url_for("usuarios.acceso"))

                session["email"] = email
                return redirect(url_for("index"))

            flash("Email o contraseña incorrecta.", "error")
            return redirect(url_for("usuarios.acceso"))

    return render_template("login.html")


# Obtenemos el usuario logueado y su rol
@usuario_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    """Permite a los usuarios ver y editar su perfil."""

    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("usuarios.acceso"))

    if not usuario.estado:
        flash(
            "Tu cuenta ha sido desactivada. Por favor, contacta con el administrador.",
            "error",
        )
        return redirect(url_for("usuarios.acceso"))

    if request.method == "POST":
        if "editar" in request.form:
            nombre_completo = request.form.get("nombre-completo", "").strip()
            foto_perfil = request.form.get("foto-perfil", "").strip()
            email = request.form.get("email", "").strip().lower()
            contraseña = request.form.get("contraseña", "").strip()

            # Si no se han realizado cambios en el perfil mandamos un mensaje
            # y redirigimos al perfil
            if not nombre_completo and not foto_perfil and not email and not contraseña:
                flash("No se han realizado cambios en el perfil.", "info")
                return redirect(url_for("usuarios.perfil"))

            # Validación de los campos para actualizar solo los que se han modificado
            nuevo_nombre = nombre_completo or usuario.nombre_completo
            nueva_foto = foto_perfil or usuario.foto_perfil
            nuevo_email = email or usuario.email
            nueva_contraseña = (
                pbkdf2_sha256.hash(contraseña) if contraseña else usuario.contraseña
            )

            gestor_bd.ejecutar_consulta(
                ACTUALIZAR_USUARIO,
                (
                    nuevo_nombre,
                    nueva_foto,
                    nuevo_email,
                    nueva_contraseña,
                    usuario.id,
                ),
            )
            flash("Perfil actualizado correctamente.", "success")

            if contraseña or email:
                session.pop(
                    "email", None
                )  # Cerrar sesión si se cambia la contraseña o el email

        return redirect(url_for("usuarios.perfil"))

    kwargs = {
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email,
        "fecha_registro": usuario.fecha_registro,
        "num_marcadores": obtener_numero_marcadores(usuario.id),
        "foto_perfil": usuario.foto_perfil,
        "rol": usuario.rol,
    }

    return render_template("perfil.html", **kwargs)


@usuario_bp.route("/mod-cuenta/<accion>/<id_usuario>")
def modificar_cuenta(accion, id_usuario):
    """Permite a los administradores eliminar o bloquear/desbloquear cuentas de usuario."""

    admin = usr_sesion()
    # Si NO hay un usuario logueado
    if not isinstance(admin, UsuarioBD):
        flash("Debes iniciar sesión para realizar esta acción.", "error")
        return redirect(url_for("usuarios.acceso"))

    usuario = obtener_usuario_por_id(id_usuario)
    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        flash(
            "El usuario que intentas modificar no existe o ha sido eliminado.",
            "error",
        )
        return redirect(url_for("index"))

    # Si el usuario logueado es ADMIN
    elif admin.rol != "admin":
        flash(
            "Los usuarios normales no pueden eliminar una cuenta.",
            "error",
        )
        return redirect(url_for("index"))

    match accion:
        case "eliminar":
            try:
                gestor_bd.ejecutar_consulta(BORRAR_USUARIO, (usuario.id,))
                session.pop(usuario.email, None)  # Eliminar la sesión del usuario
                flash("Cuenta eliminada correctamente.", "success")
                return redirect(url_for("index"))
            except Exception as e:
                flash(f"Error al eliminar la cuenta: {str(e)}", "error")
                return redirect(url_for("index"))

        case "invertir_estado":
            if usuario.estado:
                mensaje = "Cuenta bloqueada correctamente."
            else:
                mensaje = "Cuenta desbloqueada correctamente."

            try:
                gestor_bd.ejecutar_consulta(
                    MODIFICAR_ESTADO_USUARIO, (not usuario.estado, usuario.id)
                )

                flash(mensaje, "success")
                session.pop(
                    usuario.email, None
                )  # Eliminar la sesión del usuario si se bloquea

                return redirect(url_for("index"))
            except Exception as e:
                flash(f"Error al actualizar el estado de la cuenta: {str(e)}", "error")
                return redirect(url_for("index"))

    flash("Acción no válida.", "error")
    return redirect(url_for("index"))
