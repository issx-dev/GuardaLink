import logging
from datetime import datetime

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logs = logging


def error_logs(msg):
    logs.error(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ❌ {msg}")


def info_logs(msg):
    logs.info(f"{datetime.today().strftime('%Y-%m-%d %H:%M:%S')} ✅ {msg}")
