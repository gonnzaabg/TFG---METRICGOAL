from .Jugador import Jugador
from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase que representa a un jugador de la cantera de nuestro club.
      Hereda los atributos básicos de la superclase Jugador.
"""

class Canterano(Jugador):

    # @param id_jugador: Identificador único del jugador (int)
    # @param nombre: Nombre del jugador (string)
    # @param apellido: Apellidos del jugador (string)
    # @param edad: Edad del jugador en años (int)
    # @param posicion: Posición principal en el terreno de juego (string)
    def __init__(self, id_jugador, nombre, apellido, edad, posicion):
        # Llamamos al constructor de la clase padre (Jugador)
        super().__init__(id_jugador, nombre, apellido, edad, posicion)

    # --- MÉTODOS DE LÓGICA ---
    
    # @def: Visualiza la evolución de las estadísticas del canterano a lo largo del tiempo
    def ver_evolucion(self):
        # TODO: Implementar lógica de consulta a Estadisticas_Temporada
        pass

    # @def: Vincula un nuevo registro de estadísticas al canterano
    def vincular_estadisticas(self):
        # TODO: Implementar lógica de inserción de estadísticas
        pass

    @staticmethod
    def guardar_en_db(id_equipo, nombre, apellidos, edad, posicion):
        # IMPORTANTE: Solo 5 columnas, el id_jugador se llena solo por el DEFAULT de arriba
        sql = """
            INSERT INTO jugadores (id_equipo, nombre, apellidos, edad, posicion) 
            VALUES (?, ?, ?, ?, ?)
        """
        params = (id_equipo, nombre, apellidos, edad, posicion)
        return ejecutar_consulta(sql, params)

    @staticmethod
    def obtener_por_equipo(id_equipo):
        sql = "SELECT nombre, apellidos, posicion FROM jugadores WHERE id_equipo = ?"
        return ejecutar_consulta(sql, (id_equipo,)) 