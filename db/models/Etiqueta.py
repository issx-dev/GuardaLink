class EtiquetaInsert:
    def __init__(self, nombre, id_marcador):
        self.__nombre = nombre
        self.__id_marcador = id_marcador

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def id_marcador(self):
        return self.__id_marcador
    
    @property
    def obtener_datos(self):
        return (self.__nombre, self.__id_marcador)


class EtiquetaBD(EtiquetaInsert):
    def __init__(self, id, nombre, id_marcador):
        super().__init__(nombre, id_marcador)
        self.__id = id

    @property
    def id(self):
        return self.__id
