##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from db.utils.consultas import (
    obtener_usuario_completo,
    crear_marcadores_y_etiquetas_por_defecto,
    obtener_numero_marcadores,
    obtener_marcadores,
)
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioInsert, UsuarioBD, Usuario  # noqa: F401
from settings import (
    SECRET_KEY,
    INSERTAR_USUARIO,
    CONSULTA_USUARIO,  # noqa: F401
    CONSULTA_USUARIO_COMPLETO,  # noqa: F401
)


app = Flask(__name__)
app.secret_key = SECRET_KEY


##
@app.route("/")
def index():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not usuario:
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    else:
        marcadores = obtener_marcadores(usuario.id)  # type: ignore
        return render_template(
            "index.html",
            foto_perfil=usuario.foto_perfil,  # type: ignore
            marcadores=marcadores,
        )


# CRUD DE USUARIOS
# Inicio de sesión y registro de nuevos usuarios
@app.route("/acceso", methods=["GET", "POST"])
def acceso():
    if request.method == "POST":
        # Obtiene los datos del formulario html
        nombre_completo = request.form.get("nombre-completo", "").strip()
        email = request.form.get("email", "").strip().lower()
        contraseña = request.form.get("contraseña", "")

        if not email or not contraseña:
            flash("Por favor, rellena todos los campos obligatorios.", "error")
            return redirect(url_for("acceso"))

        # Obtiene la instancia usuario de la sesión actual
        usuario_actual = obtener_usuario_completo(email)

        # Registro
        if "registrarse" in request.form:
            if usuario_actual:
                flash(
                    "Este email ya está registrado, por favor Inicie Sesión.", "error"
                )
                return redirect(url_for("acceso"))

            # Inserción de usuario en la BD
            usr = UsuarioInsert(nombre_completo, pbkdf2_sha256.hash(contraseña), email)
            gestor_bd.ejecutar_consulta(
                INSERTAR_USUARIO,
                usr.obtener_datos,
            )

            usuario_actual = obtener_usuario_completo(email)
            crear_marcadores_y_etiquetas_por_defecto(usuario_actual.id)  # type: ignore

            session["email"] = email
            return redirect(url_for("index"))

        # Inicio de sesión
        elif "iniciar-sesion" in request.form:
            if usuario_actual and pbkdf2_sha256.verify(
                contraseña,
                usuario_actual.contraseña,  # type: ignore
            ):
                session["email"] = email
                return redirect(url_for("index"))

            flash("Email o contraseña incorrecta.", "error")
            return redirect(url_for("acceso"))

    return render_template("login.html")


# Obtenemos el usuario logueado y su rol
@app.route("/perfil")
def perfil():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not usuario:
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":  # type: ignore
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    else:
        datos = {
            "nombre_completo": usuario.nombre_completo,  # type: ignore
            "email": usuario.email,  # type: ignore
            "fecha_registro": usuario.fecha_registro,  # type: ignore
            "num_marcadores": obtener_numero_marcadores(usuario.id),  # type: ignore
            "foto_perfil": usuario.foto_perfil,  # type: ignore
        }

        return render_template("perfil.html", **datos)

# Actualización del perfil de usuario
@app.route("/editar-perfil", methods=["POST"])
def editar_perfil():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not usuario:
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":  # type: ignore
        return "Eres admin"

    # Si el usuario logueado es NORMAL obtenemos los datos del formulario
    nombre_completo = request.form.get("nombre-completo", "").strip()
    foto_perfil = request.form.get("foto-perfil", "").strip()
    email = request.form.get("email", "").strip().lower()
    contraseña = request.form.get("contraseña", "").strip()

    # Si no se han realizado cambios en el perfil mandamos un mensaje
    # y redirigimos al perfil
    if not nombre_completo and not foto_perfil and not email and not contraseña:
        flash("No se han realizado cambios en el perfil.", "info")
        return redirect(url_for("perfil"))

    # Validación de los campos para actualizar solo los que se han modificado
    nuevo_nombre = nombre_completo or usuario.nombre_completo  # type: ignore
    nueva_foto = foto_perfil or usuario.foto_perfil  # type: ignore
    nuevo_email = email or usuario.email  # type: ignore
    nueva_contraseña = (
        pbkdf2_sha256.hash(contraseña) if contraseña else usuario.contraseña  # type: ignore
    )

    gestor_bd.ejecutar_consulta(
        """
        UPDATE usuarios
        SET nombre_completo = ?, foto_perfil = ?, email = ?, contraseña = ?
        WHERE id = ?
        """,
        (
            nuevo_nombre,
            nueva_foto,
            nuevo_email,
            nueva_contraseña,
            usuario.id,  # type: ignore
        ),
    )
    flash("Perfil actualizado correctamente.", "success")

    if contraseña or email:
        session.pop(
            "email", None
        )  # Cerrar sesión si se cambia la contraseña o el email

    return redirect(url_for("perfil"))


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("email", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)
