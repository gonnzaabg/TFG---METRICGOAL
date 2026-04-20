from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase base que representa a un jugador general (Superclase). 
      De ella heredarán las clases Canterano y Profesional.
"""

class Jugador:

    # @param id_jugador: Identificador único del jugador (int)
    # @param nombre: Nombre del jugador (string)
    # @param apellido: Apellidos del jugador (string)
    # @param edad: Edad del jugador en años (int)
    # @param posicion: Posición principal en el terreno de juego (string)
    def __init__(self, id_jugador, nombre, apellido, edad, posicion):
        self.__id_jugador = id_jugador
        self.__nombre = nombre
        self.__apellido = apellido
        self.__edad = edad
        self.__posicion = posicion

    # --- GETTERS ---
    
    # @return: Devuelve el ID del jugador
    @property
    def id_jugador(self):
        return self.__id_jugador

    # @return: Devuelve el nombre del jugador
    @property
    def nombre(self):
        return self.__nombre

    # @return: Devuelve los apellidos del jugador
    @property
    def apellido(self):
        return self.__apellido

    # @return: Devuelve la edad del jugador
    @property
    def edad(self):
        return self.__edad

    # @return: Devuelve la posición del jugador
    @property
    def posicion(self):
        return self.__posicion

    # --- SETTERS ---
    
    # Nota: No se incluye setter para id_jugador por ser clave primaria inmutable.

    # @param valor: Nuevo nombre a asignar
    @nombre.setter
    def nombre(self, valor):
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__nombre = valor.strip()
        else:
            print("Error: El nombre no puede estar vacío.")

    # @param valor: Nuevo apellido a asignar
    @apellido.setter
    def apellido(self, valor):
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__apellido = valor.strip()
        else:
            print("Error: El apellido no puede estar vacío.")

    # @param valor: Nueva edad a asignar
    @edad.setter
    def edad(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__edad = valor
        else:
            print("Error: La edad debe ser un número entero positivo.")

    # @param valor: Nueva posición a asignar
    @posicion.setter
    def posicion(self, valor):
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__posicion = valor.strip()
        else:
            print("Error: La posición no puede estar vacía.")