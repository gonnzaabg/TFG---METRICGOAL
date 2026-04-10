import soccerdata as sd
import duckdb
import time

# 1. Configurar conexión
con = duckdb.connect('metricgoal.duckdb')

# 2. Lista de las 5 grandes ligas (nombres exactos para Understat)
ligas_top = [
    "ESP-La Liga", 
    "ENG-Premier League", 
    "GER-Bundesliga", 
    "ITA-Serie A", 
    "FRA-Ligue 1"
]

def descargar_todo_understat():
    for liga in ligas_top:
        print(f"--- Descargando todos los jugadores de: {liga} ---")
        try:
            # En Understat, seasons=2023 corresponde a la 23/24
            ud = sd.Understat(leagues=liga, seasons=2023)
            df = ud.read_player_season_stats().reset_index()
            
            # Limpiamos nombres de columnas (quitar puntos o espacios si los hay)
            df.columns = [c.replace('.', '_').replace(' ', '_').lower() for c in df.columns]
            
            # Guardamos en una tabla única para todas las ligas
            # Si la tabla no existe, la crea. Si existe, añade los datos (append).
            con.execute("CREATE TABLE IF NOT EXISTS todos_los_jugadores AS SELECT * FROM df WHERE 1=0")
            con.execute("INSERT INTO todos_los_jugadores SELECT * FROM df")
            
            print(f"Éxito: {len(df)} jugadores añadidos de {liga}.")
            
            # Pausa corta (Understat aguanta bien, con 5-10s sobra)
            time.sleep(5)
            
        except Exception as e:
            print(f"Error en {liga}: {e}")

if __name__ == "__main__":
    # Opcional: Borrar la tabla anterior si quieres empezar de cero y evitar duplicados
    con.execute("DROP TABLE IF EXISTS todos_los_jugadores")
    descargar_todo_understat()
    con.close()
    print("\n¡Base de datos completada con las 5 grandes ligas!")