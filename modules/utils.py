import logging
from datetime import datetime
from flask import session


# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logs = logging


def error_logs(msg):
    logs.error(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ❌ {msg}")


def info_logs(msg):
    logs.info(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ✅ {msg}")

def usr_sesion():
    from db.utils.consultas import obtener_usuario_completo
    # Obtiene el usuario logueado y su rol
    email_sesion = session.get("email")
    usuario = obtener_usuario_completo(email_sesion)

    return usuario