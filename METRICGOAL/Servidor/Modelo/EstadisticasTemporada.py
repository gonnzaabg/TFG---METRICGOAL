from Modelo.database import ejecutar_consulta

class EstadisticasTemporada:
    def __init__(self, id_jugador, temporada, goles, asistencias, amarillas, rojas, partidos, minutos, pases_clave):
        self.id_jugador = id_jugador
        self.temporada = temporada
        self.goles = goles
        self.asistencias = asistencias
        self.amarillas = amarillas
        self.rojas = rojas
        self.partidos = partidos
        self.minutos = minutos
        self.pases_clave = pases_clave

    @staticmethod
    def guardar_estadisticas(id_jugador, d):
        # 'd' es el diccionario con los datos
        sql = """
            INSERT INTO estadisticas_temporada 
            (id_jugador, temporada, goles, asistencias, tarj_amarillas, tarj_rojas, partidos_jugados, minutos_jugados, pases_clave)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (id_jugador, temporada) 
            DO UPDATE SET 
                goles = excluded.goles,
                asistencias = excluded.asistencias,
                tarj_amarillas = excluded.tarj_amarillas,
                tarj_rojas = excluded.tarj_rojas,
                partidos_jugados = excluded.partidos_jugados,
                minutos_jugados = excluded.minutos_jugados,
                pases_clave = excluded.pases_clave
        """
        parametros = (
            id_jugador, d['temporada'], d['goles'], d['asistencias'], 
            d['tarj_amarillas'], d['tarj_rojas'], d['partidos_jugados'], 
            d['minutos_jugados'], d['pases_clave']
        )
        return ejecutar_consulta(sql, parametros)