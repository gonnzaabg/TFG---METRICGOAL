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
            # 1. Ejecutamos la consulta
            resultado = con.execute(sql, params)
            
            # 2. Si la consulta es un SELECT, devolvemos el DataFrame
            if sql.strip().upper().startswith("SELECT"):
                return resultado.df()
            
            # 3. Si es INSERT, UPDATE o DELETE, no llamamos a .df()
            # Solo confirmamos que se ejecutó devolviendo algo que no sea None
            return True 
            
        except Exception as e:
            print(f"❌ Error en la consulta SQL: {e}")
            return None
        finally:
            con.close()
    return None