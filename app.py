# Importa las librerías necesarias
from flask import Flask, render_template, redirect, session, url_for

# Blueprints (Rutas de la aplicación)
from blueprints.usuarios import usuario_bp
from blueprints.marcadores import marcador_bp
from blueprints.buscador import buscador_bp

# Importa las consultas y funciones necesarias
from db.queries.etiquetas import ETIQUETAS_MAS_USADAS
from settings import SECRET_KEY
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioBD
from modules.utils import usr_sesion
from db.utils.consultas import obtener_marcadores_y_etiquetas


# Inicializa la aplicación Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Registrar blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(marcador_bp)
app.register_blueprint(buscador_bp)


# Ruta principal
@app.route("/")
def index():
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("usuarios.acceso"))

    # Si el usuario logueado es ADMIN
    if usuario.rol == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
    marcadores = obtener_marcadores_y_etiquetas(usuario.id)
    etiquetas_mas_usadas = gestor_bd.ejecutar_consulta(
        ETIQUETAS_MAS_USADAS, (usuario.id,)
    )
    return render_template(
        "index.html",
        foto_perfil=usuario.foto_perfil,
        marcadores=marcadores,
        etiquetas_mas_usadas=etiquetas_mas_usadas,
    )


# Ruta error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Ruta para cerrar sesión
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("email", None)
    return redirect(url_for("index"))


# Ejecuta la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
