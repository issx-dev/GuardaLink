from db.BaseDatos import gestor_bd


def obtener_rol(email):
    """
    Función para obtener el rol de un usuario a partir de su correo electrónico.
    """
    consulta = "SELECT rol FROM usuarios WHERE email = ?"
    resultado = gestor_bd.ejecutar_consulta(consulta, (email,))

    if resultado:
        return resultado[0][0]
    else:
        return None
