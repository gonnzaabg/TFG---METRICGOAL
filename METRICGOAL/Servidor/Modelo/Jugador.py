from .database import ejecutar_consulta


class Jugador:
    """
    Clase base que representa a un jugador general.
    De ella heredan las clases Canterano y Profesional.
    """

    def __init__(self, id_jugador, nombre, apellido, edad, posicion):
        """
        Inicializa un jugador con sus datos básicos de identificación.
        """
        self.__id_jugador = id_jugador
        self.__nombre = nombre
        self.__apellido = apellido
        self.__edad = edad
        self.__posicion = posicion

    @property
    def id_jugador(self):
        """
        Devuelve el identificador único del jugador. No tiene setter al ser clave primaria inmutable.
        """
        return self.__id_jugador

    @property
    def nombre(self):
        """
        Devuelve el nombre del jugador.
        """
        return self.__nombre

    @property
    def apellido(self):
        """
        Devuelve los apellidos del jugador.
        """
        return self.__apellido

    @property
    def edad(self):
        """
        Devuelve la edad del jugador.
        """
        return self.__edad

    @property
    def posicion(self):
        """
        Devuelve la posición del jugador en el terreno de juego.
        """
        return self.__posicion

    @nombre.setter
    def nombre(self, valor):
        """
        Actualiza el nombre si es una cadena no vacía.
        """
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__nombre = valor.strip()
        else:
            print("Error: El nombre no puede estar vacío.")

    @apellido.setter
    def apellido(self, valor):
        """
        Actualiza los apellidos si es una cadena no vacía.
        """
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__apellido = valor.strip()
        else:
            print("Error: El apellido no puede estar vacío.")

    @edad.setter
    def edad(self, valor):
        """
        Actualiza la edad si es un entero positivo.
        """
        if isinstance(valor, int) and valor > 0:
            self.__edad = valor
        else:
            print("Error: La edad debe ser un número entero positivo.")

    @posicion.setter
    def posicion(self, valor):
        """
        Actualiza la posición si es una cadena no vacía.
        """
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__posicion = valor.strip()
        else:
            print("Error: La posición no puede estar vacía.")