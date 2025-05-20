# LIBRARIES
from decouple import config, UndefinedValueError
from modules.utils import info_logs

# ENV VARIABLES
try:
    DATABASE_NAME = config("DB_NAME", cast=str)
except UndefinedValueError as e:
    raise UndefinedValueError(
        f"No se ha definido la variable de entorno DB_NAME Detalles: {e} "
    )

info_logs("La variable de entorno DB_NAME se ha definido correctamente.")
