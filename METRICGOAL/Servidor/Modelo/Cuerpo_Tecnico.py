from .database import ejecutar_consulta


class CuerpoTecnico:
    """
    Representa al personal del staff técnico de un equipo.
    """

    def __init__(self, id_cuerpo_tecnico, id_equipo, nombre, apellidos, email, contrasenia):
        """
        Inicializa un miembro del cuerpo técnico con sus datos de identificación y acceso.
        """
        self.__id_cuerpo_tecnico = id_cuerpo_tecnico
        self.__id_equipo = id_equipo
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__email = email
        self.__contrasenia = contrasenia

    @property
    def id_cuerpo_tecnico(self):
        """
        Devuelve el identificador único del miembro del cuerpo técnico.
        """
        return self.__id_cuerpo_tecnico

    @property
    def id_equipo(self):
        """
        Devuelve el identificador del equipo al que pertenece.
        """
        return self.__id_equipo

    @property
    def nombre(self):
        """
        Devuelve el nombre del usuario.
        """
        return self.__nombre

    @property
    def apellidos(self):
        """
        Devuelve los apellidos del usuario.
        """
        return self.__apellidos

    @property
    def email(self):
        """
        Devuelve el email del usuario.
        """
        return self.__email

    @property
    def contrasenia(self):
        """
        Devuelve la contraseña del usuario (uso interno).
        """
        return self.__contrasenia

    @id_equipo.setter
    def id_equipo(self, valor):
        """
        Actualiza el equipo asignado si el valor es un entero positivo.
        """
        if isinstance(valor, int) and valor > 0:
            self.__id_equipo = valor
        else:
            print("Error: El ID del equipo debe ser un número entero positivo.")

    @nombre.setter
    def nombre(self, valor):
        """
        Actualiza el nombre si no está vacío.
        """
        if len(valor.strip()) > 0:
            self.__nombre = valor
        else:
            print("Error: El nombre no puede estar vacío.")

    @email.setter
    def email(self, valor):
        """
        Actualiza el email si tiene un formato válido.
        """
        if "@" in valor:
            self.__email = valor
        else:
            print("Error: Formato de email no válido.")

    @contrasenia.setter
    def contrasenia(self, valor):
        """
        Actualiza la contraseña si tiene al menos 4 caracteres.
        """
        if len(valor) >= 4:
            self.__contrasenia = valor
        else:
            print("Error: La contraseña debe tener al menos 4 caracteres.")

    def login(self):
        """
        Valida las credenciales del usuario contra la base de datos.
        Devuelve True si el email y contraseña existen, False en caso contrario.
        """
        sql = "SELECT * FROM cuerpo_tecnico WHERE email = ? AND contrasenia = ?"
        params = (self.__email, self.__contrasenia)
        resultado = ejecutar_consulta(sql, params)
        return resultado is not None and not resultado.empty

    def crear_comparativa(self):
        """
        Crea una nueva comparativa entre un canterano y un profesional.
        """
        pass

    def aniadir_canterano(self):
        """
        Registra un nuevo canterano en el sistema.
        """
        pass

    def eliminar_canterano(self):
        """
        Elimina un canterano del sistema.
        """
        pass

    def modificar_canterano(self):
        """
        Modifica los datos de un canterano existente.
        """
        pass