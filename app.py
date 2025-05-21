##
from flask import Flask, render_template, request, redirect, session, url_for
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = "clave_secreta"

# Diccionario temporal para almacenar usuarios
usuarios = []  # TODO BD


##
@app.route("/")
def index():
    user = session.get("usuario")

    # Si hay un usuario logueado
    if user:
        return render_template("index.html")

    # Si NO hay un usuario logueado
    return redirect(url_for("acceso"))


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
                    return "Este email ya esta registrado"

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
                return "Email o contraseña incorrecta"

    return render_template("login.html")


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("usuario", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)
