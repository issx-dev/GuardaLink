##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from settings import SECRET_KEY
from db.utils.consultas import obtener_rol


app = Flask(__name__)
app.secret_key = SECRET_KEY

# Diccionario temporal para almacenar usuarios
usuarios = []  # TODO BD


##
@app.route("/")
def index():
    user = session.get("usuario")

    rol_usuario = obtener_rol(user) if user else None

    # Si hay un usuario logueado
    if rol_usuario is None:
        return redirect(url_for("acceso"))
    elif rol_usuario == "admin":
        return "Eres admin"
    else:
        return render_template("index.html")


##
@app.route("/acceso", methods=["GET", "POST"])
def acceso():
    if request.method == "POST":
        # Obtiene los datos del formulario html
        nombre_completo = request.form.get("nombre-completo")
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")

        # Registro
        if "registrarse" in request.form:
            for usuario in usuarios:
                if usuario["email"] == email:  # TODO BD
                    flash("Este email ya está registrado, inicie sesión", "error")
                    return redirect(url_for("acceso"))

            else:
                usuarios.append(
                    {  # TODO BD
                        "nombre_completo": nombre_completo,
                        "email": email,
                        "contraseña": pbkdf2_sha256.hash(
                            contraseña
                        ),  # Encripta la pass al subirla
                    }
                )

                session["usuario"] = email
                return redirect(url_for("index"))

        # Inicio de sesión
        elif "iniciar-sesion" in request.form:
            for usuario in usuarios:
                if usuario["email"] == email and pbkdf2_sha256.verify(
                    contraseña, usuario["contraseña"]
                ):  # TODO BD
                    session["usuario"] = email
                    return redirect(url_for("index"))

            else:
                flash("Email o contraseña incorrecta", "error")
                return redirect(url_for("acceso"))

    return render_template("login.html")


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("usuario", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)
