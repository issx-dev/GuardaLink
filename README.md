# GuardaLink

GuardaLink es una aplicación web desarrollada con Flask que permite a los usuarios gestionar y organizar sus marcadores web (bookmarks) de manera eficiente.

## Características

- Sistema de autenticación de usuarios
- Gestión de marcadores web personalizados
- Sistema de etiquetado para organizar marcadores
- Búsqueda de marcadores
- Panel de administración
- Interfaz intuitiva y responsive

## Requisitos

- Python 3.x
- Flask 3.1.1
- Jinja2 3.1.6
- python-decouple 3.8
- passlib 1.7.4

## Estructura del Proyecto

```
GuardaLink/
├── app.py                 # Archivo principal de la aplicación
├── blueprints/           # Módulos de rutas de la aplicación
│   ├── usuarios.py       # Gestión de usuarios
│   ├── marcadores.py     # Gestión de marcadores
│   └── buscador.py       # Funcionalidad de búsqueda
├── db/                   # Capa de base de datos
├── static/              # Archivos estáticos
├── templates/           # Plantillas HTML
├── modules/            # Módulos auxiliares
└── settings.py         # Configuración de la aplicación
```

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python3 -m venv .venv`
3. Activar el entorno virtual:
   - Linux/Mac: `source .venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Copiar `.env.example` a `.env` y configurar las variables de entorno
6. Ejecutar la aplicación: `python3 app.py`

## Uso

1. Registrar una cuenta de usuario
2. Iniciar sesión en el sistema
3. Comenzar a añadir y organizar marcadores
4. Utilizar etiquetas para categorizar los marcadores
5. Usar el buscador para encontrar marcadores específicos

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Autores

Proyecto desarrollado por:
- Mohamed Kadi
- Francisco Cortés
- Issa El Mokadem
