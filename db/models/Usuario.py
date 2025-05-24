#   Modelo de usuario que se va a recuperar de la base de datos sin contraseña
class Usuario:
    def __init__(
        self,
        id: int,
        nombre_completo: str,
        rol: str,
        email: str,
        estado: bool,
        foto_perfil: str,
        fecha_registro: str,
    ):
        self.__id = id
        self.__nombre_completo = nombre_completo

        self.__rol = rol
        self.__email = email
        self.__estado = estado
        self.__foto_perfil = foto_perfil
        self.__fecha_registro = fecha_registro

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def nombre_completo(self):
        return self.__nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, nuevo_valor):
        self.__nombre_completo = nuevo_valor

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, value):
        if value in ["usuario", "admin"]:
            self.__rol = value
        else:
            raise ValueError("Rol inválido. Debe ser 'usuario' o 'admin'")

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, nuevo_valor):
        self.__email = nuevo_valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, value):
        if self.rol != "admin":
            raise PermissionError(
                "Solo un admin puede modificar el estado del usuario."
            )
        if value not in [True, False]:
            raise ValueError("El estado debe ser True o False.")
        self.__estado = value

    @property
    def foto_perfil(self):
        return self.__foto_perfil

    @foto_perfil.setter
    def foto_perfil(self, value):
        self.__foto_perfil = value

    # Getter para la fecha de registro, no tiene settter ya que se va a plantear como inmutable
    @property
    def fecha_registro(self):
        return self.__fecha_registro

    def obtener_info_usuario(self):
        return [
            self.id,
            self.nombre_completo,
            self.rol,
            self.email,
            self.estado,
            self.foto_perfil,
        ]

    def __str__(self):
        return f" ~ Nombre Completo: {self.nombre_completo} ~ Email: {self.email} ~ Rol: {self.rol} ~ Estado: {self.estado} ~ Foto de Perfil: {self.foto_perfil}"


#   Modelo de usuario que se va a recuperar de la base de datos con contraseña
class UsuarioBD(Usuario):
    def __init__(
        self,
        id: int,
        nombre_completo: str,
        contraseña: str,
        rol: str,
        email: str,
        estado: bool,
        foto_perfil: str,
        fecha_registro: str,
    ):
        super().__init__(
            id, nombre_completo, rol, email, estado, foto_perfil, fecha_registro
        )

        self.__contraseña = contraseña

    @property
    def contraseña(self):
        return self.__contraseña

    @contraseña.setter
    def contraseña(self, value):
        if self.rol != "admin":
            raise PermissionError("Solo un admin puede cambiar la contraseña.")

        self.__contraseña = value

    def obtener_info_usuario(self):
        return super().obtener_info_usuario() + [self.contraseña]


#   Modelo de usuario que se va a añadir a la base de datos
class UsuarioInsert:
    def __init__(
        self,
        nombre_completo: str,
        contraseña: str,
        email: str,
    ):
        self.__nombre_completo = nombre_completo
        self.__contraseña = contraseña
        self.__email = email
        

    @property
    def nombre_completo(self):
        return self.__nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, value):
        self.__nombre_completo = value

    # Getter de la contraseña, no tiene setter ya que esta clase solo sirve para insertar
    @property
    def contraseña(self):
        return self.__contraseña

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def obtener_datos(self):
        return (
            self.nombre_completo,
            self.contraseña,
            self.email,
        )
