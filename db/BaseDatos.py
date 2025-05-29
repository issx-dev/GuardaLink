#   MÓDULOS Y LIBRERÍAS
import sqlite3 as sq
from modules.utils import info_logs, error_logs
from settings import DATABASE_NAME, CREAR_TABLAS, CREAR_ROOT, INFO_ROOT


class BaseDeDatos:
    def __init__(self):
        self._inicializar_base()

    def _inicializar_base(self):
        try:
            with sq.connect(DATABASE_NAME) as conexion:
                cursor = conexion.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.executescript(CREAR_TABLAS)
                cursor.execute(CREAR_ROOT, INFO_ROOT)
                conexion.commit()
                info_logs(" -> Conexión establecida correctamente")
        except sq.Error as e:
            error_logs(f" !-> Error al conectar con la base de datos: {e}")
            raise

    def ejecutar_consulta(
        self, consulta, parametros=None, many=False, retornar_id=False
    ):
        if parametros is None:
            parametros = []

        try:
            with sq.connect(DATABASE_NAME) as conexion:
                cursor = conexion.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")

                if many:
                    cursor.executemany(consulta, parametros)
                    conexion.commit()
                    return cursor.fetchall()
                else:
                    cursor.execute(consulta, parametros)
                    last_id = cursor.lastrowid if retornar_id else None
                    conexion.commit()
                    return last_id if retornar_id else cursor.fetchall()

        except sq.Error as e:
            error_logs(
                f" !-> Error al ejecutar la consulta de base de datos. DETALLES: {e}"
            )
            return False


# Instancia global
gestor_bd = BaseDeDatos()
