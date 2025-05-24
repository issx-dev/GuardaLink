##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from db.utils.consultas import (
    obtener_usuario_completo,
    crear_marcadores_y_etiquetas_por_defecto,
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
    usuario = obtener_usuario_completo(email_sesion) if email_sesion else None

    # Si NO hay un usuario logueado
    if not usuario:
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    else:
        return render_template("index.html")


##
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


@app.route("/perfil")
def perfil():
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion) if email_sesion else None

    # Si NO hay un usuario logueado
    if not usuario:
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    else:
        datos = {  # TODO Estableces los datos del usuario logueado
            "nombre_completo": "Mercedes Cortés Perez",
            "email": "mercedescortesperez12@gmail.com",
            "fecha_registro": "29/05/2025",
            "num_marcadores": 99,
            "foto_perfil": "https://www.dzoom.org.es/wp-content/uploads/2020/02/portada-foto-perfil-redes-sociales-consejos.jpg",
        }

        return render_template("perfil.html", **datos)


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("email", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)