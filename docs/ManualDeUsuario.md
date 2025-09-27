## Introducción

GuardaLink es una web diseñada para gestionar y organizar tus marcadores web. Con esta herramienta podrás guardar y buscar fácilmente todos tus enlaces favoritos.

### Características principales:
- Gestión completa de marcadores web
- Sistema de etiquetas
- Búsqueda de marcadores
- Interfaz adaptada a diferentes dispositivos
- Sistema de usuarios con roles de usuario y administrador

## Acceso y Navegación

### URL de acceso
- **Desarrollo**: `http://localhost:5000`
- **Producción**: `https://guardalink.onrender.com`

### Instrucciones de Login

#### Registro
1. Accede a la página principal de la aplicación
2. Haz clic en "Registrarse" 
3. Completa el formulario con:
   - **Nombre completo**: Tu nombre y apellidos
   - **Email**: Dirección de correo electrónico válida
   - **Contraseña**: Contraseña segura
4. Haz clic en "Registrarse"
5. Si el registro es exitoso, serás redirigido automáticamente al panel principal

#### Inicio de sesión
1. En la página principal, completa:
   - **Email**: Tu dirección de correo registrada
   - **Contraseña**: Tu contraseña
2. Haz clic en "Iniciar Sesión"
3. Serás redirigido al panel principal con tus marcadores

#### Navegación principal
- **Panel Principal**: Vista general de tus marcadores organizados
- **Perfil**: Gestión de tu información personal
- **Buscador**: Herramienta de búsqueda
- **Panel Admin** (solo administradores): Gestión de usuarios del sistema

### Crear Marcadores

#### Añadir un nuevo marcador
1. Desde el panel principal, haz clic en **"Añadir Marcador"**
2. Completa el formulario:
   - **Nombre**: Título del marcador
   - **Enlace (URL)**: Dirección web completa
   - **Descripción**: Breve descripción del contenido
   - **Etiquetas**: Etiquetas separadas por comas
3. Haz clic en **"Guardar Marcador"**
4. El marcador aparecerá en tu panel principal

### Leer/Visualizar Marcadores

#### Panel principal
- **Vista de cuadrícula**: Los marcadores se muestran como tarjetas organizadas
- **Información de las tarjetas**: Nombre, descripción, etiquetas y fecha de creación
- **Acceso directo**: Haz clic en el nombre del marcador para abrir el enlace
- **Filtro de etiquetas**: Etiquetas más usadas

### Actualizar Marcadores

#### Editar un marcador existente
1. Haz clic en el botón **"Editar"** (ícono de lápiz)
2. Modifica los campos que necesites:
   - Nombre del marcador
   - URL del enlace
   - Descripción
   - Etiquetas (separadas por comas)
3. Haz clic en **"Actualizar Marcador"**

### Eliminar Marcadores

#### Borrar un marcador
1. Haz clic en el botón **"Eliminar"** (ícono de papelera)
2. **Confirma la acción** - Esta operación no se puede deshacer
3. El marcador desaparecerá inmediatamente de tu lista

## Búsqueda y Filtrado

### Buscador general
1. Utiliza la **barra de búsqueda** en el panel principal
2. Los resultados se mostrarán automáticamente

### Filtrado por etiquetas
1. En el panel **"Etiquetas más usadas"**, haz clic en cualquier etiqueta
2. Se mostrarán solo los marcadores que contengan esa etiqueta

## Gestión de Perfil

### Actualizar información personal
1. Haz clic en **"Perfil"** en el menú de navegación
2. Modifica los campos que necesites:
   - **Nombre completo**
   - **Foto de perfil**: URL de una imagen
   - **Email**: Nueva dirección de correo
   - **Contraseña**: Nueva contraseña
3. Haz clic en **"Actualizar Perfil"**

### Información del perfil
En la página de perfil podrás ver:
- Fecha de registro en el sistema
- Número total de marcadores guardados
- Información personal actual

**PD**: Si cambias tu email o contraseña, deberás iniciar sesión nuevamente.

### Gestión de usuarios
Los administradores tienen acceso a funciones especiales:

#### Ver usuarios del sistema
- Lista completa de usuarios registrados
- Estado de cada cuenta (activa/inactiva)
- Información básica de cada usuario

#### Gestionar cuentas de usuario
1. **Bloquear/Desbloquear usuarios**:
   - Haz clic en "Bloquear" para desactivar una cuenta
   - Haz clic en "Desbloquear" para reactivar una cuenta
   
2. **Eliminar usuarios**:
   - Haz clic en "Eliminar" para borrar permanentemente una cuenta
   - Esta acción eliminará también todos los marcadores del usuario

## Preguntas Frecuentes (FAQ)

### ¿Hay límite en el número de marcadores?
No hay un límite establecido.

### ¿Qué pasa si olvido mi contraseña?
Actualmente no hay sistema de recuperación de contraseña implementado. Contacta al administrador.

### ¿Puedo usar la aplicación en dispositivos móviles?
Sí, la interfaz se adapta a diferentes tamaños de pantalla.

### ¿Los marcadores se guardan automáticamente?
Sí, todos los cambios se guardan inmediatamente en la base de datos.

## Consejos y Advertencias

### Buenas prácticas

#### Para organizar marcadores:
- **Descripciones útiles**: Añade descripciones que te ayuden a recordar el contenido
- **URLs completas**: Siempre incluye http:// o https:// en las direcciones

#### Para gestionar etiquetas:
- **Categorías amplias**: Combina etiquetas específicas con generales ("python, programación")

#### Para la seguridad:
- **Contraseñas seguras**: Usa contraseñas robustas con letras, números y símbolos
- **Cierra sesión**: Especialmente en dispositivos compartidos
- **Actualiza tu información**: Mantén tu email actualizado para futuras funcionalidades

### Errores a evitar

#### Gestión de marcadores:
- ❌ **URLs incompletas** que no funcionarán al hacer clic
- ❌ **Eliminar marcadores sin confirmar** - La acción es irreversible

#### Gestión de usuarios (administradores):
- ❌ **Eliminar usuarios sin avisar** - Pueden perder trabajo importante