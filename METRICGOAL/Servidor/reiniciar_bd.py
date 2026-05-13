from pathlib import Path
import os
import random
import pandas as pd
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Data" / "metricgoal.duckdb"
CSV_PATH = BASE_DIR / "BD_METRICGOAL.csv"

print("DB_PATH =", DB_PATH)
print("EXISTS =", DB_PATH.exists())

def obtener_conexion():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))

def borrar_base_si_existe():
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("🗑️ Base de datos anterior eliminada.")
    else:
        print("ℹ️ No existía base previa.")

def crear_tablas(con):
    con.execute("CREATE TABLE club (id_club INTEGER PRIMARY KEY, nombre VARCHAR NOT NULL)")
    con.execute("""
        CREATE TABLE equipo (
            id_equipo INTEGER PRIMARY KEY,
            id_club INTEGER,
            categoria VARCHAR,
            FOREIGN KEY (id_club) REFERENCES club(id_club)
        )
    """)
    con.execute("""
        CREATE TABLE cuerpo_tecnico (
            id_cuerpo_tecnico INTEGER PRIMARY KEY,
            id_equipo INTEGER,
            nombre VARCHAR,
            apellidos VARCHAR,
            email VARCHAR UNIQUE,
            password VARCHAR,
            FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
        )
    """)
    con.execute("CREATE SEQUENCE seq_jugadores_id START 1")
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
    con.execute("CREATE SEQUENCE seq_estadisticas_id START 1")
    con.execute("""
        CREATE TABLE estadisticas_temporada (
            id_estadistica INTEGER DEFAULT nextval('seq_estadisticas_id') PRIMARY KEY,
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
    con.execute("CREATE SEQUENCE seq_informes_id START 1")
    con.execute("""
        CREATE TABLE informes (
            id_informe INTEGER DEFAULT nextval('seq_informes_id') PRIMARY KEY,
            id_equipo INTEGER NOT NULL,
            fecha VARCHAR NOT NULL,
            temporada VARCHAR NOT NULL,
            canterano VARCHAR NOT NULL,
            profesional VARCHAR NOT NULL,
            datos_json VARCHAR NOT NULL,
            FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
        )
    """)

def cargar_clubes_desde_csv(con):
    if not CSV_PATH.exists():
        print(f"❌ No se encontró {CSV_PATH}")
        return
    df = pd.read_csv(CSV_PATH)
    clubes = df["team"].dropna().drop_duplicates().tolist()
    id_actual = 2
    for nombre in clubes:
        nombre = str(nombre).strip()
        if nombre:
            con.execute("INSERT INTO club VALUES (?, ?)", (id_actual, nombre))
            id_actual += 1
    print(f"✅ Clubes cargados: {id_actual - 1}")

def crear_equipo_base(con):
    con.execute("INSERT INTO equipo VALUES (1, 1, 'Senior A')")
    print("✅ Equipo base creado.")

def generar_equipos(con):
    clubes = con.execute("SELECT id_club FROM club WHERE id_club > 1 ORDER BY id_club").fetchall()
    max_id = con.execute("SELECT COALESCE(MAX(id_equipo), 0) FROM equipo").fetchone()[0]
    nuevo_id = max_id + 1
    categorias = ["Filial", "Juvenil A", "Juvenil B"]
    for (id_club,) in clubes:
        for categoria in categorias:
            con.execute("INSERT INTO equipo VALUES (?, ?, ?)", (nuevo_id, id_club, categoria))
            nuevo_id += 1
    print("✅ Equipos generados.")

def generar_cuerpo_tecnico(con):
    nombres = [
        "Carlos","Miguel","David","John","Paul","Marco","Luca","Jean","Pierre","Hans","Thomas",
        "Alejandro","Javier","William","James","Alessandro","Giovanni","Antoine","Louis","Lukas","Felix","Hugo",
        "Diego","Daniel","Pablo","Sergio","Jorge","Mario","Luigi","Francesco","Antonio","Roberto",
        "Michael","Robert","Richard","Joseph","Charles","Marcel","Luc","Julien","Klaus","Stefan","Dieter","Jürgen","Arthur"
    ]
    apellidos = [
        "García","Martínez","Smith","Johnson","Rossi","Bianchi","Dupont","Martin","Müller","Weber",
        "López","Gómez","Williams","Brown","Romano","Colombo","Bernard","Richard","Schmidt","Wagner",
        "Fernández","Pérez","Rodríguez","Sánchez","Jones","Taylor","Davies","Evans","Ricci","Marino",
        "Greco","Gallo","Petit","Roux","Leroy","Moreau","Becker","Hoffmann","Schäfer","Koch"
    ]
    equipos = con.execute("SELECT id_equipo FROM equipo ORDER BY id_equipo").fetchall()
    max_id = con.execute("SELECT COALESCE(MAX(id_cuerpo_tecnico), 0) FROM cuerpo_tecnico").fetchone()[0]
    nuevo_id = max_id + 1
    for (id_equipo,) in equipos:
        for rol in ["Primer Entrenador", "Segundo Entrenador"]:
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            email = f"{nombre[:3].lower()}{apellido.lower()}{nuevo_id}@metricgoal.com"
            con.execute("""
                INSERT INTO cuerpo_tecnico
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nuevo_id, id_equipo, nombre, f"{apellido} ({rol})", email, "metricg0al.1234"))
            nuevo_id += 1
    print("✅ Cuerpo técnico generado.")

def validar_huérfanos(con):
    consultas = {
        "cuerpo_tecnico": "SELECT DISTINCT id_equipo FROM cuerpo_tecnico WHERE id_equipo NOT IN (SELECT id_equipo FROM equipo)",
        "jugadores": "SELECT DISTINCT id_equipo FROM jugadores WHERE id_equipo NOT IN (SELECT id_equipo FROM equipo)",
        "informes": "SELECT DISTINCT id_equipo FROM informes WHERE id_equipo NOT IN (SELECT id_equipo FROM equipo)",
        "estadisticas_temporada": "SELECT DISTINCT id_jugador FROM estadisticas_temporada WHERE id_jugador NOT IN (SELECT id_jugador FROM jugadores)",
    }
    for tabla, q in consultas.items():
        filas = con.execute(q).fetchall()
        if filas:
            print(f"⚠️ Huérfanos en {tabla}: {filas}")
        else:
            print(f"✅ {tabla} sin huérfanos.")

def main():
    borrar_base_si_existe()
    con = obtener_conexion()
    try:
        crear_tablas(con)
        con.execute("INSERT INTO club VALUES (1, 'MetricGoal F.C.')")
        crear_equipo_base(con)
        cargar_clubes_desde_csv(con)
        generar_equipos(con)
        generar_cuerpo_tecnico(con)
        validar_huérfanos(con)
        print("🎉 Base de datos rehecha desde cero con éxito.")
    finally:
        con.close()

if __name__ == "__main__":
    main()