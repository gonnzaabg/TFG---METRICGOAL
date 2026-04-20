from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase que representa a un equipo específico dentro de un club.

"""
class Equipo:
    
    # @param id_equipo: Identificador único del equipo (int)
    # @param id_club: FK del club al que pertenece (int)
    # @param categoria: Categoría del equipo (ej: Senior, Juvenil A) (string)
    def __init__(self, id_equipo, id_club, categoria):
        self.__id_equipo = id_equipo
        self.__id_club = id_club
        self.__categoria = categoria

    # --- GETTERS ---
    
    # @return: Devuelve el ID del equipo
    @property
    def id_equipo(self):
        return self.__id_equipo

    # @return: Devuelve el ID del club (FK)
    @property
    def id_club(self):
        return self.__id_club

    # @return: Devuelve la categoría del equipo
    @property
    def categoria(self):
        return self.__categoria

    # --- SETTERS ---
    
    # @param valor: Nuevo ID de club a asignar
    @id_club.setter
    def id_club(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__id_club = valor
        else:
            print("Error: El ID del club debe ser un número entero positivo.")

    # @param valor: Nueva categoría a asignar
    @categoria.setter
    def categoria(self, valor):
        if len(valor.strip()) > 0:
            self.__categoria = valor
        else:
            print("Error: La categoría no puede estar vacía.")

    # --- MÉTODOS DE LÓGICA ---
    
    # @def: Añade un nuevo canterano a este equipo
    def anadir_canterano(self):
        # TODO: Implementar lógica de inserción
        pass

    # @def: Devuelve la lista de jugadores que pertenecen al equipo
    def listar_jugadores(self):
        # TODO: Implementar lógica de búsqueda
        pass