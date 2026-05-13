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
    query = "SELECT id_jugador, nombre, apellidos, edad, posicion FROM jugadores WHERE id_equipo = ?"
    df = ejecutar_consulta(query, (id_equipo,))
    
    if df is not None and not df.empty:
        resultado = df.to_dict(orient='records')
        print(f"DEBUG jugadores: {resultado}")
        return resultado
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

def eliminar_jugador_logic(id_jugador):
    try:
        # 1. Borrar estadísticas vinculadas al jugador
        # Usamos tu función ejecutar_consulta pasando los parámetros en una tupla (id,)
        ejecutar_consulta("DELETE FROM estadisticas_temporada WHERE id_jugador = ?", (id_jugador,))
        
        # 2. Borrar al jugador de la tabla principal
        ejecutar_consulta("DELETE FROM jugadores WHERE id_jugador = ?", (id_jugador,))
        
        return {"status": "success"}
    except Exception as e:
        print(f"Error en lógica de eliminación: {e}")
        return {"status": "error", "message": str(e)}

def obtener_profesionales_busqueda(nombre: str):
    """
    Busca los profesionales que coincidan con el nombre proporcionado.
    """
    query = """
        SELECT player, team, league 
        FROM profesionales 
        WHERE player ILIKE ? 
        LIMIT 10
    """
    params = (f"%{nombre}%",)
    
    # Llamamos a la base de datos
    df = ejecutar_consulta(query, params)
    
    # Si hay resultados, devolvemos los records, si no, lista vacía
    if df is not None and not df.empty:
        return df.to_dict(orient='records')
    return []

def obtener_datos_comparativa(id_canterano, nombre_profesional, temporada="2025/26"):
    try:
        # 1. CANTERANO — filtramos por la temporada seleccionada
        query_can = """
            SELECT j.nombre, e.goles, e.asistencias, e.pases_clave, 
                   e.tarj_amarillas, e.tarj_rojas
            FROM jugadores j
            JOIN estadisticas_temporada e ON j.id_jugador = e.id_jugador
            WHERE j.id_jugador = ? AND e.temporada = ?
        """
        df_can = ejecutar_consulta(query_can, (id_canterano, temporada))
        
        # 2. PROFESIONAL
        query_pro = """
            SELECT player, goals, assists, key_passes, yellow_cards, red_cards 
            FROM profesionales WHERE player = ?
        """
        df_pro = ejecutar_consulta(query_pro, (nombre_profesional,))

        if df_can.empty or df_pro.empty:
            return {"error": "Faltan datos de alguno de los jugadores"}

        can = df_can.iloc[0]
        pro = df_pro.iloc[0]

        labels = ['Goles Totales', 'Asistencias Totales', 'Pases Clave', 'Amarillas', 'Rojas']

        can_vals = [
            int(can['goles'] or 0),
            int(can['asistencias'] or 0),
            int(can['pases_clave'] or 0),
            int(can['tarj_amarillas'] or 0),
            int(can['tarj_rojas'] or 0)
        ]

        pro_vals = [
            int(pro['goals'] or 0),
            int(pro['assists'] or 0),
            int(pro['key_passes'] or 0),
            int(pro['yellow_cards'] or 0),
            int(pro['red_cards'] or 0)
        ]

        return {
            "labels": labels,
            "canterano": {"nombre": can['nombre'], "valores": can_vals},
            "profesional": {"nombre": pro['player'], "valores": pro_vals}
        }

    except Exception as e:
        print(f"Error en comparativa totales: {e}")
        return {"error": str(e)}

def obtener_stats_destacados(id_equipo):
    goleador = ejecutar_consulta("""
        SELECT j.nombre, j.apellidos, MAX(e.goles) as goles
        FROM jugadores j
        JOIN estadisticas_temporada e ON j.id_jugador = e.id_jugador
        WHERE j.id_equipo = ?
        GROUP BY j.nombre, j.apellidos
        ORDER BY goles DESC
        LIMIT 1
    """, (id_equipo,))
    
    asistente = ejecutar_consulta("""
        SELECT j.nombre, j.apellidos, MAX(e.asistencias) as asistencias
        FROM jugadores j
        JOIN estadisticas_temporada e ON j.id_jugador = e.id_jugador
        WHERE j.id_equipo = ?
        GROUP BY j.nombre, j.apellidos
        ORDER BY asistencias DESC
        LIMIT 1
    """, (id_equipo,))
    
    return {
        "goleador": goleador.to_dict(orient='records')[0] if goleador is not None and not goleador.empty else None,
        "asistente": asistente.to_dict(orient='records')[0] if asistente is not None and not asistente.empty else None
    }

def obtener_stats_equipo(id_equipo):
    result = ejecutar_consulta("""
        SELECT 
            COUNT(DISTINCT j.id_jugador) as total_jugadores,
            COALESCE(SUM(e.goles), 0) as total_goles,
            COALESCE(SUM(e.asistencias), 0) as total_asistencias,
            COALESCE(SUM(e.partidos_jugados), 0) as total_partidos,
            COALESCE(SUM(e.pases_clave), 0) as total_pases_clave
        FROM jugadores j
        LEFT JOIN estadisticas_temporada e ON j.id_jugador = e.id_jugador
        WHERE j.id_equipo = ?
    """, (id_equipo,))
    if result is not None and not result.empty:
        return result.to_dict(orient='records')[0]
    return {"total_jugadores": 0, "total_goles": 0, "total_asistencias": 0, "total_partidos": 0, "total_pases_clave": 0}

    