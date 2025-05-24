# Clase marcador que se va a añadir a la base de datos
class MarcadorInsert:
    def __init__(self, id_usuario, nombre, enlace, descripcion):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__enlace = enlace
        self.__descripcion = descripcion

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def enlace(self):
        return self.__enlace

    @enlace.setter
    def enlace(self, value):
        self.__enlace = value

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, value):
        self.__descripcion = value

    @property
    def obtener_info_marcador(self):
        return [
            self.__id_usuario,
            self.__nombre,
            self.__enlace,
            self.__descripcion,
        ]

    def __str__(self):
        return f" Nombre:{self.__nombre}, Enlace:{self.__enlace}, Descripcion:{self.__descripcion}), ID usuario:{self.__id_usuario}"


#   Modelo de marcador que se va a recuperar de la base de datos
class MarcadorBD(MarcadorInsert):
    def __init__(self, id, id_usuario, nombre, enlace, descripcion):
        super().__init__(id_usuario, nombre, enlace, descripcion)
        self.__id = id

    @property
    def id(self):
        return self.__id
