from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase que representa a un club deportivo en el sistema.

"""
class Club:

    # @param id_club: Identificador único del club (int)
    # @param nombre: Nombre oficial del club (string)
    def __init__(self, id_club, nombre):
        self.__id_club = id_club
        self.__nombre = nombre

    # --- GETTERS ---
    
    @property
    def id_club(self):
        return self.__id_club

    @property
    def nombre(self):
        return self.__nombre

    # --- SETTERS ---
    
    @nombre.setter
    def nombre(self, valor):
        if len(valor.strip()) > 0:
            self.__nombre = valor
        else:
            print("Error: El nombre del club no puede estar vacío.")

    # --- MÉTODOS DE LÓGICA ---
    
    # @def: Devuelve un resumen con los datos básicos del club
    def obtener_informacion(self):
        return f"Club [ID: {self.__id_club}] - Nombre: {self.__nombre}"