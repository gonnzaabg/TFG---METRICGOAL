import duckdb
import os
import pandas as pd

def obtener_conexion():
    # 1. Buscamos dónde estamos exactamente (carpeta Modelo)
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Subimos dos niveles (Modelo -> Servidor -> METRICGOAL) y entramos a Data
    ruta_carpeta_data = os.path.abspath(os.path.join(directorio_actual, '..', '..', 'Data'))
    ruta_archivo_db = os.path.join(ruta_carpeta_data, 'metricgoal.duckdb')

    # 3. MAGIA: Si la carpeta 'Data' no existe, la construimos automáticamente
    if not os.path.exists(ruta_carpeta_data):
        os.makedirs(ruta_carpeta_data)
        print(f"📁 Carpeta 'Data' creada automáticamente en: {ruta_carpeta_data}")

    # 4. Conectamos (DuckDB creará el archivo automáticamente si no existe)
    try:
        con = duckdb.connect(ruta_archivo_db)
        return con
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return None

def ejecutar_consulta(sql, params=()):
    con = obtener_conexion()
    if con:
        try:
            # Ejecutamos y devolvemos un DataFrame de pandas, que es lo que espera tu código
            return con.execute(sql, params).df()
        except Exception as e:
            print(f"❌ Error en la consulta SQL: {e}")
            return None
        finally:
            con.close()
    return None