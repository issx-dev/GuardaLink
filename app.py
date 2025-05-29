# Importa las librerías necesarias
from flask import Flask, render_template, redirect, session, url_for, flash

# Blueprints (Rutas de la aplicación)
from blueprints.usuarios import usuario_bp
from blueprints.marcadores import marcador_bp
from blueprints.buscador import buscador_bp

# Importa las consultas y funciones necesarias
from db.queries.etiquetas import ETIQUETAS_MAS_USADAS
from db.queries.usuarios import CONSULTA_USUARIOS
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
    """Muestra la página de inicio con los marcadores del usuario logueado."""
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("usuarios.acceso"))

    if not usuario.estado:
        flash(
            "Tu cuenta ha sido desactivada. Por favor, contacta con el administrador.",
            "error",
        )
        session.pop("email", None)
        return redirect(url_for("usuarios.acceso"))

    # Si el usuario logueado es NORMAL
    marcadores = obtener_marcadores_y_etiquetas(usuario.id)
    etiquetas_mas_usadas = gestor_bd.ejecutar_consulta(
        ETIQUETAS_MAS_USADAS, (usuario.id,)
    )

    pagina = "admin.html" if usuario.rol == "admin" else "index.html"

    kwargs = {
        "foto_perfil": usuario.foto_perfil,
        "marcadores": marcadores,
        "etiquetas_mas_usadas": etiquetas_mas_usadas,
        "rol": usuario.rol,
    }

    if usuario.rol == "admin":
        kwargs["usuarios"] = gestor_bd.ejecutar_consulta(CONSULTA_USUARIOS)

    return render_template(pagina, **kwargs)


# Ruta error 404
@app.errorhandler(404)
def page_not_found(e):
    """Muestra una página de error 404."""
    return render_template("404.html"), 404


# Ruta para cerrar sesión
@app.route("/cerrar-sesion")
def cerrar_sesion():
    """Cierra la sesión del usuario y redirige a la página de inicio."""
    session.pop("email", None)
    return redirect(url_for("index"))


# Ejecuta la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
