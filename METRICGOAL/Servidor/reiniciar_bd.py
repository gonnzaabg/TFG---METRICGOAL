import duckdb

con = duckdb.connect("md:metricgoal_md?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImdvbnphbG9ib3UuMjAyMy5hbHVtbkBjZXNjcmlzdG9yZXkuY29tIiwibWRSZWdpb24iOiJhd3MtZXUtY2VudHJhbC0xIiwic2Vzc2lvbiI6ImdvbnphbG9ib3UuMjAyMy5hbHVtbi5jZXNjcmlzdG9yZXkuY29tIiwicGF0IjoidUg3VGdkZGxpUWxkWmFUTE9KbjhZZnlFVy1ZX3N4UDZWOWY4TGJrZzdibyIsInVzZXJJZCI6ImFkNTUyNzA0LTZiMTItNGUxMC1iNWI0LWFhMjE2NTk2OWM5YiIsImlzcyI6Im1kX3BhdCIsInJlYWRPbmx5IjpmYWxzZSwidG9rZW5UeXBlIjoicmVhZF93cml0ZSIsImlhdCI6MTc3NzM5Nzk4NH0.uf4GkffqKpWZawH0QwlxgY2FGD1EeDze66QeUBULxyc")

con.execute("DROP TABLE IF EXISTS estadisticas_temporada")
con.execute("DROP TABLE IF EXISTS informes")
con.execute("DROP TABLE IF EXISTS jugadores")
con.execute("DROP TABLE IF EXISTS cuerpo_tecnico")
con.execute("DROP TABLE IF EXISTS equipo")
con.execute("DROP TABLE IF EXISTS club")
con.execute("DROP SEQUENCE IF EXISTS seq_jugadores_id")
con.execute("DROP SEQUENCE IF EXISTS seq_estadisticas_id")
con.execute("DROP SEQUENCE IF EXISTS seq_informes_id")

con.execute("CREATE SEQUENCE seq_jugadores_id START 1")
con.execute("CREATE SEQUENCE seq_estadisticas_id START 1")
con.execute("CREATE SEQUENCE seq_informes_id START 1")

con.execute("CREATE TABLE club (id_club INTEGER PRIMARY KEY, nombre VARCHAR NOT NULL)")
con.execute("""CREATE TABLE equipo (
    id_equipo INTEGER PRIMARY KEY, id_club INTEGER, categoria VARCHAR,
    FOREIGN KEY (id_club) REFERENCES club(id_club))""")
con.execute("""CREATE TABLE cuerpo_tecnico (
    id_cuerpo_tecnico INTEGER PRIMARY KEY, id_equipo INTEGER,
    nombre VARCHAR, apellidos VARCHAR, email VARCHAR UNIQUE, password VARCHAR,
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo))""")
con.execute("""CREATE TABLE jugadores (
    id_jugador INTEGER DEFAULT nextval('seq_jugadores_id') PRIMARY KEY,
    id_equipo INTEGER, nombre VARCHAR, apellidos VARCHAR, edad INTEGER, posicion VARCHAR,
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo))""")
con.execute("""CREATE TABLE estadisticas_temporada (
    id_estadistica INTEGER DEFAULT nextval('seq_estadisticas_id') PRIMARY KEY,
    id_jugador INTEGER, temporada VARCHAR,
    goles INTEGER DEFAULT 0, asistencias INTEGER DEFAULT 0,
    tarj_amarillas INTEGER DEFAULT 0, tarj_rojas INTEGER DEFAULT 0,
    partidos_jugados INTEGER DEFAULT 0, minutos_jugados INTEGER DEFAULT 0,
    pases_clave INTEGER DEFAULT 0,
    FOREIGN KEY (id_jugador) REFERENCES jugadores(id_jugador),
    UNIQUE (id_jugador, temporada))""")
con.execute("""CREATE TABLE informes (
    id_informe INTEGER DEFAULT nextval('seq_informes_id') PRIMARY KEY,
    id_equipo INTEGER NOT NULL, fecha VARCHAR NOT NULL, temporada VARCHAR NOT NULL,
    canterano VARCHAR NOT NULL, profesional VARCHAR NOT NULL, datos_json VARCHAR NOT NULL,
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo))""")

print("🎉 BD recreada correctamente en MotherDuck")