##
from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import pbkdf2_sha256
from db.utils.consultas import (
    obtener_usuario_completo,
    crear_marcadores_y_etiquetas_por_defecto,
    obtener_numero_marcadores,
    obtener_marcadores_y_etiquetas,
    obtener_marcadores_especificos,
)
from db.BaseDatos import gestor_bd
from db.models.Usuario import UsuarioInsert, UsuarioBD
from settings import (
    ELIMINAR_MARCADOR,
    SECRET_KEY,
    INSERTAR_USUARIO,
    ACTUALIZAR_USUARIO,
    BUSCADOR_MARCADORES,
    INSERTAR_MARCADOR,
    INSERTAR_ETIQUETA,
    ETIQUETAS_MAS_USADAS,
    FILTRAR_MARCADORES_POR_ETIQUETAS,
    CONSULTA_MARCADOR,
    CONSULTA_NOMBRES_ETIQUETAS,
    ACTUALIZAR_MARCADOR,,
    BORRAR_ETIQUETA,
)
from db.models.Marcador import MarcadorInsert, MarcadorBD
from db.models.Etiqueta import EtiquetaInsert
from modules.utils import usr_sesion


app = Flask(__name__)
app.secret_key = SECRET_KEY


##
@app.route("/")
def index():
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

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
                flash(
                    "Error al registrar el usuario, por favor inténtelo de nuevo.",
                    "error",
                )
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
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        return "Eres admin"

    # Si el usuario logueado es NORMAL
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

    kwargs = {
        "nombre_completo": usuario.nombre_completo,
        "email": usuario.email,
        "fecha_registro": usuario.fecha_registro,
        "num_marcadores": obtener_numero_marcadores(usuario.id),
        "foto_perfil": usuario.foto_perfil,
    }

    return render_template("perfil.html", **kwargs)


@app.route("/mod-marcador/<accion>/<id_marcador>")
@app.route("/marcador", methods=["GET", "POST"])
def marcador(id_marcador=None, accion=None):
    usuario = usr_sesion()

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        return "Eres admin"

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
            etiquetas = etiquetas or etiquetas_nuevas

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
            for etiqueta in etiquetas:
                gestor_bd.ejecutar_consulta(INSERTAR_ETIQUETA, (etiqueta[0].strip(), id_marcador))
            
            # Mensaje de éxito
            flash("Marcador actualizado correctamente.", "success")

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

    if request.method == "POST" and "añadir" in request.form:
        # Convertimos los datos del formulario en una lista para separar las etiquetas
        datos = list(request.form.values())
        del datos[-1]  # Eliminamos el último elemento (añadir/editar del if)
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
            return redirect(url_for("marcador"))

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


# Buscador marcadores
@app.route("/buscador/<filtro_etiqueta>")
@app.route("/buscador", methods=["GET", "POST"])
def buscar_marcador(filtro_etiqueta=None):
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    # Si NO hay un usuario logueado
    if not isinstance(usuario, UsuarioBD):
        return redirect(url_for("acceso"))

    # Si el usuario logueado es ADMIN
    elif usuario.rol == "admin":
        return "Eres admin"

    etiquetas_mas_usadas = gestor_bd.ejecutar_consulta(
        ETIQUETAS_MAS_USADAS, (usuario.id,)
    )

    if filtro_etiqueta:
        resultado = gestor_bd.ejecutar_consulta(
            FILTRAR_MARCADORES_POR_ETIQUETAS, (usuario.id, f"%{filtro_etiqueta}%")
        )

        lista_IDs = []
        if isinstance(resultado, list):
            lista_IDs = [marcador[0] for marcador in resultado]
        else:
            flash(
                "No se ha encotrado ningún resultado que coincida con las búsqueda.",
                "info",
            )

        # Marcadores de la búsqueda
        marcadores = obtener_marcadores_especificos(usuario.id, lista_IDs)

        return render_template(
            "index.html",
            marcadores=marcadores,
            foto_perfil=usuario.foto_perfil,
            etiquetas_mas_usadas=etiquetas_mas_usadas,
        )

    # Busqueda de marcadores
    busqueda = request.form.get("buscador_marcadores", "").strip()
    # Formateo busqueda para SQL
    busqueda = f"%{busqueda}%"
    # Ejecutamos la consulta para buscar marcadores
    resultado = gestor_bd.ejecutar_consulta(
        BUSCADOR_MARCADORES, (usuario.id, busqueda, busqueda, busqueda)
    )

    lista_IDs = []
    if isinstance(resultado, list):
        lista_IDs = [marcador[0] for marcador in resultado]
    else:
        flash(
            "No se ha encotrado ningún resultado que coincida con las búsqueda.", "info"
        )

    # Marcadores de la búsqueda
    marcadores = obtener_marcadores_especificos(usuario.id, lista_IDs)

    return render_template(
        "index.html",
        marcadores=marcadores,
        foto_perfil=usuario.foto_perfil,
        etiquetas_mas_usadas=etiquetas_mas_usadas,
    )


##
@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("email", None)
    return redirect(url_for("index"))


####
if __name__ == "__main__":
    app.run(debug=True)
