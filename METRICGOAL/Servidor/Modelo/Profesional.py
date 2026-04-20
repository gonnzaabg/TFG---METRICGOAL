from .jugador import Jugador
from .database import ejecutar_consulta

"""
@author: gonnzaabg
@def: Clase que representa a un jugador profesional de élite.
    Hereda de Jugador y añade estadísticas de rendimiento para comparativas.
"""

class Profesional(Jugador):

    # @param id_jugador: Identificador único del jugador (int)
    # @param nombre: Nombre del jugador (string)
    # @param apellido: Apellidos del jugador (string)
    # @param edad: Edad del jugador en años (int)
    # @param posicion: Posición principal en el terreno de juego (string)
    # @param nombre_club: Club profesional al que pertenece (string)
    # @param goles: Goles marcados (int)
    # @param asistencias: Asistencias realizadas (int)
    # @param tarj_amarillas: Tarjetas amarillas recibidas (int)
    # @param tarj_rojas: Tarjetas rojas recibidas (int)
    # @param partidos_jugados: Total de partidos disputados (int)
    # @param minutos_jugados: Total de minutos disputados (int)
    # @param pases_clave: Pases clave realizados (int)
    def __init__(self, id_jugador, nombre, apellido, edad, posicion, nombre_club, goles, asistencias, tarj_amarillas, tarj_rojas, partidos_jugados, minutos_jugados, pases_clave):
        
        # Llamamos al constructor de la clase padre (Jugador)
        super().__init__(id_jugador, nombre, apellido, edad, posicion)
        
        # Inicializamos los atributos propios de Profesional
        self.__nombre_club = nombre_club
        self.__goles = goles
        self.__asistencias = asistencias
        self.__tarj_amarillas = tarj_amarillas
        self.__tarj_rojas = tarj_rojas
        self.__partidos_jugados = partidos_jugados
        self.__minutos_jugados = minutos_jugados
        self.__pases_clave = pases_clave

    # --- GETTERS ---

    @property
    def nombre_club(self): return self.__nombre_club

    @property
    def goles(self): return self.__goles

    @property
    def asistencias(self): return self.__asistencias

    @property
    def tarj_amarillas(self): return self.__tarj_amarillas

    @property
    def tarj_rojas(self): return self.__tarj_rojas

    @property
    def partidos_jugados(self): return self.__partidos_jugados

    @property
    def minutos_jugados(self): return self.__minutos_jugados

    @property
    def pases_clave(self): return self.__pases_clave

    # --- SETTERS ---
    
    @nombre_club.setter
    def nombre_club(self, valor):
        if isinstance(valor, str) and len(valor.strip()) > 0:
            self.__nombre_club = valor.strip()
        else:
            print("Error: El nombre del club no puede estar vacío.")

    @goles.setter
    def goles(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__goles = valor

    @asistencias.setter
    def asistencias(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__asistencias = valor

    @tarj_amarillas.setter
    def tarj_amarillas(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__tarj_amarillas = valor

    @tarj_rojas.setter
    def tarj_rojas(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__tarj_rojas = valor

    @partidos_jugados.setter
    def partidos_jugados(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__partidos_jugados = valor

    @minutos_jugados.setter
    def minutos_jugados(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__minutos_jugados = valor

    @pases_clave.setter
    def pases_clave(self, valor):
        if isinstance(valor, int) and valor >= 0: self.__pases_clave = valor

    # --- MÉTODOS DE LÓGICA ---
    
    # @def: Filtra jugadores profesionales según la posición ingresada
    def filtrar_posicion(self):
        # TODO: Implementar lógica de filtrado
        pass

    # @def: Carga los datos y métricas del jugador desde la base de datos externa/API
    def cargar_datos(self):
        # TODO: Implementar lógica de carga de datos
        pass