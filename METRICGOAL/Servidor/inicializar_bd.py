from Modelo.database import obtener_conexion

def preparar_base_de_datos():
    con = obtener_conexion()
    if not con:
        return

    print("🛠️ Iniciando la configuración de la base de datos...")

    try:
        # 1. CLUB
        con.execute("CREATE TABLE IF NOT EXISTS club (id_club INTEGER PRIMARY KEY, nombre VARCHAR NOT NULL)")

        # 2. EQUIPO
        con.execute("""
            CREATE TABLE IF NOT EXISTS equipo (
                id_equipo INTEGER PRIMARY KEY, 
                id_club INTEGER, 
                categoria VARCHAR,
                FOREIGN KEY (id_club) REFERENCES club(id_club)
            )
        """)

        # 3. CUERPO TÉCNICO
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

        # 4. SECUENCIA Y JUGADORES (Añadido IF NOT EXISTS)
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

        # 5. ESTADÍSTICAS (Borramos y recreamos para asegurar el UNIQUE)
        # Descomenta la línea de abajo SOLO UNA VEZ para resetearla si ves que no funciona el guardado
        # con.execute("DROP TABLE IF EXISTS estadisticas_temporada")

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
                
                -- ESTO ES LO QUE NECESITAMOS PARA EL UPSERT (ON CONFLICT)
                UNIQUE (id_jugador, temporada)
            )
        """)
        print("✅ Tabla 'estadisticas_temporada' verificada con restricción UNIQUE.")

        # --- INSERTAR DATOS DE PRUEBA ---
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