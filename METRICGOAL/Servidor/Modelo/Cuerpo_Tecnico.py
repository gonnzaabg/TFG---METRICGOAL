from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase que representa al personal del staff técnico.

"""
class CuerpoTecnico:

    # @author: gonnzaabg
    # @param id_cuerpo_tecnico: Identificador único (int)
    # @param id_equipo: FK del equipo al que pertenece (int)
    # @param nombre: Nombre del usuario (string)
    # @param apellidos: Apellidos del usuario (string)
    # @param email: Correo electrónico único (string)
    # @param contrasenia: Contraseña de acceso (string)
    def __init__(self, id_cuerpo_tecnico, id_equipo, nombre, apellidos, email, contrasenia):
        self.__id_cuerpo_tecnico = id_cuerpo_tecnico
        self.__id_equipo = id_equipo  # <-- NUEVA FK AÑADIDA
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__email = email
        self.__contrasenia = contrasenia

    # --- GETTERS ---

    # @return: Devuelve el ID del cuerpo técnico
    @property
    def id_cuerpo_tecnico(self):
        return self.__id_cuerpo_tecnico

    # @return: Devuelve el ID del equipo (FK)
    @property
    def id_equipo(self):
        return self.__id_equipo

    # @return: Devuelve el nombre del usuario
    @property
    def nombre(self):
        return self.__nombre

    # @return: Devuelve los apellidos del usuario
    @property
    def apellidos(self):
        return self.__apellidos

    # @return: Devuelve el email del usuario
    @property
    def email(self):
        return self.__email

    # @return: Devuelve la contraseña (uso interno)
    @property
    def contrasenia(self):
        return self.__contrasenia

    # --- SETTERS ---

    # @param valor: Nuevo ID de equipo a asignar
    @id_equipo.setter
    def id_equipo(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__id_equipo = valor
        else:
            print("Error: El ID del equipo debe ser un número entero positivo.")

    # @param valor: Nuevo nombre a asignar
    @nombre.setter
    def nombre(self, valor):
        if len(valor.strip()) > 0:
            self.__nombre = valor
        else:
            print("Error: El nombre no puede estar vacío.")

    # @param valor: Nuevo email a asignar
    @email.setter
    def email(self, valor):
        if "@" in valor:
            self.__email = valor
        else:
            print("Error: Formato de email no válido.")

    # @param valor: Nueva contraseña (mínimo 4 caracteres)
    @contrasenia.setter
    def contrasenia(self, valor):
        if len(valor) >= 4:
            self.__contrasenia = valor
        else:
            print("Error: La contraseña debe tener al menos 4 caracteres.")

    # --- MÉTODOS DE LÓGICA ---

    # @def: Realiza la validación del usuario contra la base de datos
    # @return: True si las credenciales existen, False en caso contrario
    def login(self):
        sql = "SELECT * FROM cuerpo_tecnico WHERE email = ? AND contrasenia = ?"
        params = (self.__email, self.__contrasenia)
        resultado = ejecutar_consulta(sql, params)
        return resultado is not None and not resultado.empty

    # @def: Crea una nueva comparativa entre canterano y profesional
    def crear_comparativa(self):
        pass

    # @def: Registra un nuevo canterano en el sistema
    def aniadir_canterano(self):
        pass

    # @def: Elimina un canterano del sistema
    def eliminar_canterano(self):
        pass

    # @def: Modifica los datos de un canterano existente
    def modificar_canterano(self):
        pass