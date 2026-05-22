from .database import ejecutar_consulta


class Equipo:
    """
    Representa a un equipo específico dentro de un club.
    """

    def __init__(self, id_equipo, id_club, categoria):
        """
        Inicializa un equipo con su identificador, club al que pertenece y categoría.
        """
        self.__id_equipo = id_equipo
        self.__id_club = id_club
        self.__categoria = categoria

    @property
    def id_equipo(self):
        """
        Devuelve el identificador único del equipo.
        """
        return self.__id_equipo

    @property
    def id_club(self):
        """
        Devuelve el identificador del club al que pertenece el equipo.
        """
        return self.__id_club

    @property
    def categoria(self):
        """
        Devuelve la categoría del equipo (ej: Senior, Juvenil A).
        """
        return self.__categoria

    @id_club.setter
    def id_club(self, valor):
        """
        Actualiza el club asignado si el valor es un entero positivo.
        """
        if isinstance(valor, int) and valor > 0:
            self.__id_club = valor
        else:
            print("Error: El ID del club debe ser un número entero positivo.")

    @categoria.setter
    def categoria(self, valor):
        """
        Actualiza la categoría si no está vacía.
        """
        if len(valor.strip()) > 0:
            self.__categoria = valor
        else:
            print("Error: La categoría no puede estar vacía.")

    def anadir_canterano(self):
        """
        Añade un nuevo canterano a este equipo.
        """
        # TODO: Implementar lógica de inserción
        pass

    def listar_jugadores(self):
        """
        Devuelve la lista de jugadores que pertenecen al equipo.
        """
        # TODO: Implementar lógica de búsqueda
        pass