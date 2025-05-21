##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from settings import SECRET_KEY
from db.utils.consultas import obtener_rol
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioInsert, UsuarioBD, Usuario
from settings import INSERTAR_USUARIO, CONSULTA_USUARIO, CONSULTA_USUARIO_COMPLETO


app = Flask(__name__)
app.secret_key = SECRET_KEY


##
@app.route("/")
def index():
    # Obtiene el usuario logueado y su rol
    user = session.get("usuario")
    rol_usuario = obtener_rol(user)

    # Si NO hay un usuario logueado
    if rol_usuario == None:
        return redirect(url_for("acceso"))
    
    # Si el usuario logueado es ADMIN
    elif rol_usuario == "admin":
        return "Eres admin"
    
    # Si el usuario logueado es NORMAL
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

        # Recuperción de los usuarios como instancias de la clase UsuarioBD
        consulta_completa_resultado = gestor_bd.ejecutar_consulta(CONSULTA_USUARIO_COMPLETO)
        if isinstance(consulta_completa_resultado, list):
            usuarios = [UsuarioBD(*usr) for usr in consulta_completa_resultado]
        else:
            usuarios = []
        

        # Registro
        if "registrarse" in request.form:
            for usuario in usuarios:
                if usuario.email == email:
                    flash("Este email ya está registrado, por favor Inicie Sesión.", "error")
                    return redirect(url_for("acceso"))

            else:
                # Inserción de usuario en la BD
                usr = UsuarioInsert(nombre_completo, pbkdf2_sha256.hash(contraseña), email)
                gestor_bd.ejecutar_consulta(
                    INSERTAR_USUARIO,
                    usr.obtener_datos,
                )

                session["usuario"] = email
                return redirect(url_for("index"))

        # Inicio de sesión
        elif "iniciar-sesion" in request.form:
            for usuario in usuarios:
                if usuario.email == email and pbkdf2_sha256.verify(
                    contraseña, usuario.contraseña
                ):
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
