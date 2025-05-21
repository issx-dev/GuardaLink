#   MÓDULOS Y LIBRERÍAS
import sqlite3 as sq
from modules.utils import info_logs, error_logs
from settings import DATABASE_NAME, CREAR_TABLAS, CREAR_ROOT, INFO_ROOT


class BaseDeDatos:
    def __init__(self):
        try:
            self.__conexion = sq.connect(DATABASE_NAME)
            self.__cursor = self.__conexion.cursor()
            self.__cursor.execute("PRAGMA foreign_keys = ON")
            self.__cursor.execute(CREAR_TABLAS)
            self.__cursor.execute(CREAR_ROOT, INFO_ROOT)
            info_logs(" -> Conexión establecida correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al conectar con la base de datos: {e}")
            raise

    def ejecutar_consulta(self, consulta, parametros=None, many=False):
        if parametros is None:
            parametros = []

        try:
            if many:
                self.__cursor.executemany(consulta, parametros)
            else:
                self.__cursor.execute(consulta, parametros)

            self.__conexion.commit()
            return self.__cursor.fetchall()

        except sq.Error as e:
            error_logs(
                f" !-> Error al ejecutar la consulta de base de datos. DETALLES: {e}"
            )
            self.revertir_cambios()
            return False

    def guardar_cambios(self):
        try:
            self.__conexion.commit()
            info_logs(" -> Cambios guardados correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al guardar los cambios: {e}")
            self.revertir_cambios()

    def revertir_cambios(self):
        try:
            self.__conexion.rollback()
            info_logs(" -> Cambios revertidos correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al revertir los cambios: {e}")

    def cerrar_conexion(self):
        try:
            self.__conexion.close()
            info_logs(" -> Conexión cerrada correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al cerrar la conexión: {e}")


# Instancia global
gestor_bd = BaseDeDatos()
