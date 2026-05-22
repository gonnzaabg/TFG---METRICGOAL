from .database import ejecutar_consulta


class Club:
    """
    Representa a un club deportivo en el sistema.
    """

    def __init__(self, id_club, nombre):
        """
        Inicializa un club con su identificador y nombre oficial.
        """
        self.__id_club = id_club
        self.__nombre = nombre

    @property
    def id_club(self):
        """
        Devuelve el identificador único del club.
        """
        return self.__id_club

    @property
    def nombre(self):
        """
        Devuelve el nombre oficial del club.
        """
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """
        Actualiza el nombre del club si no está vacío.
        """
        if len(valor.strip()) > 0:
            self.__nombre = valor
        else:
            print("Error: El nombre del club no puede estar vacío.")

    def obtener_informacion(self):
        """
        Devuelve un resumen con los datos básicos del club.
        """
        return f"Club [ID: {self.__id_club}] - Nombre: {self.__nombre}"