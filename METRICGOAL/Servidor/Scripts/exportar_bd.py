import duckdb

# 1. Conectamos a tu base de datos local
con = duckdb.connect('metricgoal.duckdb')

try:
    print("Exportando datos a CSV...")
    
    # 2. Sentencia mágica de DuckDB para exportar
    # Esto creará un archivo llamado 'todos_los_jugadores_2324.csv' en tu carpeta
    con.execute("COPY todos_los_jugadores TO 'metricgoal_profesionales.csv' (HEADER, DELIMITER ',')")
    
    print("¡Hecho! El archivo 'metricgoal_profesionales.csv' ya está en tu carpeta.")

except Exception as e:
    print(f"Error al exportar: {e}")
    # Si la tabla tiene otro nombre, prueba a ver cuáles hay primero:
    # tablas = con.execute("SHOW TABLES").df()
    # print(tablas)

finally:
    con.close()