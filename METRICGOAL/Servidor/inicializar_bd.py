import os
from Modelo.database import obtener_conexion

def preparar_base_de_datos():
    con = obtener_conexion()
    if not con:
        return

    print("🛠️ Iniciando la configuración de la base de datos...")

    try:
        # --- TABLAS EXISTENTES ---
        con.execute("CREATE TABLE IF NOT EXISTS club (id_club INTEGER PRIMARY KEY, nombre VARCHAR NOT NULL)")
        con.execute("""
            CREATE TABLE IF NOT EXISTS equipo (
                id_equipo INTEGER PRIMARY KEY, 
                id_club INTEGER, 
                categoria VARCHAR,
                FOREIGN KEY (id_club) REFERENCES club(id_club)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS cuerpo_tecnico (
                id_cuerpo_tecnico INTEGER PRIMARY KEY,
                id_equipo INTEGER,
                nombre VARCHAR,
                apellidos VARCHAR,
                email VARCHAR UNIQUE,
                password VARCHAR,
                FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
            )
        """)
        con.execute("CREATE SEQUENCE IF NOT EXISTS seq_jugadores_id START 1")
        con.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id_jugador INTEGER DEFAULT nextval('seq_jugadores_id') PRIMARY KEY,
                id_equipo INTEGER,
                nombre VARCHAR,
                apellidos VARCHAR,
                edad INTEGER,
                posicion VARCHAR,
                FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS estadisticas_temporada (
                id_estadistica INTEGER DEFAULT nextval('seq_jugadores_id') PRIMARY KEY,
                id_jugador INTEGER,
                temporada VARCHAR,
                goles INTEGER DEFAULT 0,
                asistencias INTEGER DEFAULT 0,
                tarj_amarillas INTEGER DEFAULT 0,
                tarj_rojas INTEGER DEFAULT 0,
                partidos_jugados INTEGER DEFAULT 0,
                minutos_jugados INTEGER DEFAULT 0,
                pases_clave INTEGER DEFAULT 0,
                FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador),
                UNIQUE (id_jugador, temporada)
            )
        """)

        # --- SECCIÓN NUEVA: TABLA PROFESIONALES ---
        # Comprobamos si la tabla existe
        res = con.execute("SELECT count(*) FROM information_schema.tables WHERE table_name = 'profesionales'").fetchone()
        
        if res[0] == 0:
            print("📦 La tabla 'profesionales' no existe. Iniciando importación desde CSV...")
            
            # Buscamos el CSV (usamos una ruta relativa robusta para Render)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Asegúrate de que esta ruta coincida con donde está el CSV en GitHub
            # Si el CSV está en la raíz, quita "Scripts"
            ruta_csv = os.path.join(base_dir, "Scripts", "BD_METRICGOAL - Hoja 1.csv")

            if os.path.exists(ruta_csv):
                sql_importar = f"""
                    CREATE TABLE profesionales AS 
                    SELECT * FROM read_csv('{ruta_csv}', 
                        header=True, 
                        delim=',', 
                        quote='"',
                        ignore_errors=True)
                """
                con.execute(sql_importar)
                print("✅ Tabla 'profesionales' creada y cargada desde CSV.")
            else:
                print(f"❌ ERROR: No se encontró el CSV en {ruta_csv}. La comparación no funcionará.")

        # --- DATOS DE PRUEBA ---
        con.execute("INSERT OR IGNORE INTO club (id_club, nombre) VALUES (1, 'MetricGoal F.C.')")
        con.execute("INSERT OR IGNORE INTO equipo (id_equipo, id_club, categoria) VALUES (1, 1, 'Senior A')")
        con.execute("""
            INSERT OR IGNORE INTO cuerpo_tecnico (id_cuerpo_tecnico, id_equipo, nombre, apellidos, email, password) 
            VALUES (1, 1, 'Gonzalo', 'Admin', 'admin@metricgoal.com', '1234')
        """)

    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
    finally:
        con.close()