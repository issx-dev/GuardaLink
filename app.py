##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from db.utils.consultas import (
    obtener_usuario_completo,
    crear_marcadores_y_etiquetas_por_defecto,
    obtener_numero_marcadores,
    obtener_marcadores_y_etiquetas,
)
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioInsert, UsuarioBD
from settings import SECRET_KEY, INSERTAR_USUARIO, ACTUALIZAR_USUARIO


app = Flask(__name__)
app.secret_key = SECRET_KEY


##
@app.route("/")
def index():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    else:
        marcadores = obtener_marcadores_y_etiquetas(usuario.id)
        print(marcadores[0])
        return render_template(
            "index.html",
            foto_perfil=usuario.foto_perfil,
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
            if isinstance(usuario_actual, UsuarioBD):
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
            if not isinstance(usuario_actual, UsuarioBD):
                flash("Error al registrar el usuario, por favor inténtelo de nuevo.", "error")
                return redirect(url_for("acceso"))
            crear_marcadores_y_etiquetas_por_defecto(usuario_actual.id) 

            session["email"] = email
            return redirect(url_for("index"))

        # Inicio de sesión
        elif "iniciar-sesion" in request.form:
            if isinstance(usuario_actual, UsuarioBD) and pbkdf2_sha256.verify(
                contraseña,
                usuario_actual.contraseña,
            ):
                session["email"] = email
                return redirect(url_for("index"))

            flash("Email o contraseña incorrecta.", "error")
            return redirect(url_for("acceso"))

    return render_template("login.html")


# Obtenemos el usuario logueado y su rol
@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        return "Eres admin"

    if request.method == "POST":
        if "editar" in request.form:
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

        return redirect(url_for("perfil"))

    # Si el usuario logueado es NORMAL
    kwargs = {
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email,
        "fecha_registro": usuario.fecha_registro,
        "num_marcadores": obtener_numero_marcadores(usuario.id),
        "foto_perfil": usuario.foto_perfil,
    }

    return render_template("perfil.html", **kwargs)


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("email", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)
