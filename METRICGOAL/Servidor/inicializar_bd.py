from Modelo.database import obtener_conexion

def preparar_base_de_datos():
    con = obtener_conexion()
    if not con:
        # Si la conexión falla (por ejemplo, si no existe la carpeta Data), salimos
        return

    print("🛠️ Iniciando la configuración de la base de datos...")

    try:
        # 1. CREAR TABLA CLUB (El Abuelo)
        con.execute("""
            CREATE TABLE IF NOT EXISTS club (
                id_club INTEGER PRIMARY KEY,
                nombre VARCHAR NOT NULL
            )
        """)
        print("✅ Tabla 'club' creada.")

        # 2. CREAR TABLA EQUIPO (El Padre)
        con.execute("""
            CREATE TABLE IF NOT EXISTS equipo (
                id_equipo INTEGER PRIMARY KEY,
                id_club INTEGER,
                categoria VARCHAR,
                FOREIGN KEY (id_club) REFERENCES club(id_club)
            )
        """)
        print("✅ Tabla 'equipo' creada y vinculada al Club.")

        # 3. CREAR TABLA CUERPO TECNICO (El Hijo)
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
        print("✅ Tabla 'cuerpo_tecnico' creada y vinculada al Equipo.")

        # 1. Borramos la tabla vieja
        #con.execute("DROP TABLE IF EXISTS jugadores")

        # 2. Creamos una SECUENCIA (el contador automático)
        con.execute("CREATE SEQUENCE IF NOT EXISTS seq_jugadores_id START 1")

        # 3. Creamos la tabla vinculando el ID a esa secuencia
        con.execute("""
            CREATE TABLE jugadores (
                id_jugador INTEGER DEFAULT nextval('seq_jugadores_id') PRIMARY KEY,
                id_equipo INTEGER,
                nombre VARCHAR,
                apellidos VARCHAR,
                edad INTEGER,
                posicion VARCHAR,
                FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
            )
        """)
        print("✅ Tabla 'jugadores' reseteada con Secuencia Automática.")

        # --- INSERTAR DATOS DE PRUEBA EN ORDEN ---
        
        # 1º El Club
        con.execute("INSERT OR IGNORE INTO club (id_club, nombre) VALUES (1, 'MetricGoal F.C.')")
        
        # 2º El Equipo (Vinculado al Club 1)
        con.execute("INSERT OR IGNORE INTO equipo (id_equipo, id_club, categoria) VALUES (1, 1, 'Senior A')")
        
        # 3º El Cuerpo Técnico (Tú, vinculado al Equipo 1)
        con.execute("""
            INSERT OR IGNORE INTO cuerpo_tecnico (id_cuerpo_tecnico, id_equipo, nombre, apellidos, email, password) 
            VALUES (1, 1, 'Gonzalo', 'Admin', 'admin@metricgoal.com', '1234')
        """)
        print("✅ Datos de prueba insertados (Club, Equipo y tu Usuario Admin).")


    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    preparar_base_de_datos()