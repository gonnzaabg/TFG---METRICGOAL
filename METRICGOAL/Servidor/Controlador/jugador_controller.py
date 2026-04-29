from Modelo.Canterano import Canterano
from Modelo.database import ejecutar_consulta
from Modelo.EstadisticasTemporada import EstadisticasTemporada

# Le cambiamos el nombre a la función para que sea único
def gestionar_registro_canterano(datos_validados, id_equipo):
    try:
        Canterano.guardar_en_db(
            id_equipo,
            datos_validados.nombre, 
            datos_validados.apellidos, 
            datos_validados.edad, 
            datos_validados.posicion
        )
        return {"status": "success"}
    except Exception as e:
        print(f"Error en controlador: {e}")
        return {"status": "error", "message": str(e)}

def listar_jugadores_logic(id_equipo):
    ejecutar_consulta("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id_jugador INTEGER DEFAULT nextval('seq_jugadores_id') PRIMARY KEY,
            id_equipo INTEGER,
            nombre VARCHAR,
            apellidos VARCHAR,
            edad INTEGER,
            posicion VARCHAR
        )
    """)
    
    query = "SELECT id_jugador, nombre, apellidos, posicion FROM jugadores WHERE id_equipo = ?"
    df = ejecutar_consulta(query, (id_equipo,))
    
    if df is not None and not df.empty:
        return df.to_dict(orient='records')
    return []

def obtener_stats_jugador_temporada(id_jugador, temporada):
    query = """
        SELECT goles, asistencias, tarj_amarillas, tarj_rojas, 
               partidos_jugados, minutos_jugados, pases_clave 
        FROM estadisticas_temporada 
        WHERE id_jugador = ? AND temporada = ?
    """
    df = ejecutar_consulta(query, (id_jugador, temporada))
    
    if df is not None and not df.empty:
        return df.to_dict(orient='records')[0] # Devolvemos la primera fila encontrada
    return None # Si no hay nada, devolvemos None


def gestionar_registro_stats(datos_validados, id_jugador):
    try:
        EstadisticasTemporada.guardar_estadisticas(id_jugador, datos_validados.dict())
        return {"status": "success"}
    except Exception as e:
        print(f"Error en controlador stats: {e}")
        return {"status": "error", "message": str(e)}

    