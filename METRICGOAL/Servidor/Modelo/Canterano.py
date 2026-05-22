from .Jugador import Jugador
from .database import ejecutar_consulta


class Canterano(Jugador):
    """
    Representa a un jugador de la cantera del club.
    Hereda los atributos básicos de la superclase Jugador.
    """

    def __init__(self, id_jugador, nombre, apellido, edad, posicion):
        """
        Inicializa un canterano llamando al constructor de la clase padre.
        """
        super().__init__(id_jugador, nombre, apellido, edad, posicion)

    def ver_evolucion(self):
        """
        Visualiza la evolución de las estadísticas del canterano a lo largo del tiempo.
        """
        # TODO: Implementar lógica de consulta a Estadisticas_Temporada
        pass

    def vincular_estadisticas(self):
        """
        Vincula un nuevo registro de estadísticas al canterano.
        """
        # TODO: Implementar lógica de inserción de estadísticas
        pass

    @staticmethod
    def guardar_en_db(id_equipo, nombre, apellidos, edad, posicion):
        """
        Inserta un nuevo canterano en la base de datos asociado a un equipo.
        Usa una secuencia para generar el id_jugador automáticamente.
        """
        sql = """
            INSERT INTO jugadores (id_jugador, id_equipo, nombre, apellidos, edad, posicion) 
            VALUES (nextval('seq_jugadores_id'), ?, ?, ?, ?, ?)
        """
        params = (id_equipo, nombre, apellidos, edad, posicion)
        return ejecutar_consulta(sql, params)

    @staticmethod
    def obtener_por_equipo(id_equipo):
        """
        Devuelve el nombre, apellidos y posición de todos los canteranos de un equipo.
        """
        sql = "SELECT nombre, apellidos, posicion FROM jugadores WHERE id_equipo = ?"
        return ejecutar_consulta(sql, (id_equipo,))