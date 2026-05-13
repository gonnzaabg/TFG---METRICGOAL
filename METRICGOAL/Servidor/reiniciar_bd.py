import duckdb

con = duckdb.connect("md:metricgoal_md")
con.execute("ATTACH 'C:\\Users\\Gonzalo\\Desktop\\TFG---METRICGOAL\\METRICGOAL\\Data\\metricgoal.duckdb' AS local_db (READ_ONLY)")

tablas = ["club", "equipo", "cuerpo_tecnico", "jugadores", "estadisticas_temporada", "informes"]
for tabla in tablas:
    con.execute(f"CREATE OR REPLACE TABLE {tabla} AS SELECT * FROM local_db.main.{tabla}")
    print(f"✅ {tabla} copiada")

print("🎉 Listo")