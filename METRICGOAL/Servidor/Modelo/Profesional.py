from .jugador import Jugador
from .database import ejecutar_consulta


class Profesional(Jugador):
    """
    Representa a un jugador profesional de élite.
    Hereda de Jugador y añade estadísticas de rendimiento para comparativas.
    """

    def __init__(self, id_jugador, nombre, apellido, edad, posicion, nombre_club, goles, asistencias, tarj_amarillas, tarj_rojas, partidos_jugados, minutos_jugados, pases_clave):
        """
        Inicializa un jugador profesional con sus datos básicos heredados de Jugador
        y sus estadísticas de rendimiento propias.
        """
        super().__init__(id_jugador, nombre, apellido, edad, posicion)
        self.__nombre_club = nombre_club
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarj_amarillas = tarj_amarillas
        self.__tarj_rojas = tarj_rojas
        self.__partidos_jugados = partidos_jugados
        self.__minutos_jugados = minutos_jugados
        self.__pases_clave = pases_clave

    @property
    def nombre_club(self):
        """Devuelve el club profesional al que pertenece el jugador."""
        return self.__nombre_club

    @property
    def goles(self):
        """Devuelve el total de goles marcados."""
        return self.__goles

    @property
    def asistencias(self):
        """Devuelve el total de asistencias realizadas."""
        return self.__asistencias

    @property
    def tarj_amarillas(self):
        """Devuelve el total de tarjetas amarillas recibidas."""
        return self.__tarj_amarillas

    @property
    def tarj_rojas(self):
        """Devuelve el total de tarjetas rojas recibidas."""
        return self.__tarj_rojas

    @property
    def partidos_jugados(self):
        """Devuelve el total de partidos disputados."""
        return self.__partidos_jugados

    @property
    def minutos_jugados(self):
        """Devuelve el total de minutos disputados."""
        return self.__minutos_jugados

    @property
    def pases_clave(self):
        """Devuelve el total de pases clave realizados."""
        return self.__pases_clave

    @nombre_club.setter
    def nombre_club(self, valor):
        """Actualiza el club si es una cadena no vacía."""
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__nombre_club = valor.strip()
        else:
            print("Error: El nombre del club no puede estar vacío.")

    @goles.setter
    def goles(self, valor):
        """Actualiza los goles si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__goles = valor

    @asistencias.setter
    def asistencias(self, valor):
        """Actualiza las asistencias si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__asistencias = valor

    @tarj_amarillas.setter
    def tarj_amarillas(self, valor):
        """Actualiza las tarjetas amarillas si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__tarj_amarillas = valor

    @tarj_rojas.setter
    def tarj_rojas(self, valor):
        """Actualiza las tarjetas rojas si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__tarj_rojas = valor

    @partidos_jugados.setter
    def partidos_jugados(self, valor):
        """Actualiza los partidos jugados si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__partidos_jugados = valor

    @minutos_jugados.setter
    def minutos_jugados(self, valor):
        """Actualiza los minutos jugados si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__minutos_jugados = valor

    @pases_clave.setter
    def pases_clave(self, valor):
        """Actualiza los pases clave si el valor es un entero no negativo."""
        if isinstance(valor, int) and valor >= 0: self.__pases_clave = valor

    def filtrar_posicion(self):
        """
        Filtra jugadores profesionales según la posición ingresada.
        """
        # TODO: Implementar lógica de filtrado
        pass

    def cargar_datos(self):
        """
        Carga los datos y métricas del jugador desde la base de datos.
        """
        # TODO: Implementar lógica de carga de datos
        pass