import duckdb
import os
import pandas as pd

def obtener_conexion():
    # 1. Buscamos el token en las "entrañas" del servidor (Environment Variables)
    token = os.getenv("MOTHERDUCK_TOKEN")
    
    if token:
        try:
            # Conectamos usando el token que configuraremos en Render
            con = duckdb.connect(f"md:metricgoal?motherduck_token={token}")
            # Por si acaso, nos aseguramos de estar en la base de datos correcta
            con.execute("CREATE DATABASE IF NOT EXISTS metricgoal")
            con.execute("USE metricgoal")
            return con
        except Exception as e:
            print(f"❌ Error en MotherDuck: {e}")
            return None
    else:
        # --- MODO LOCAL (Tu PC / Desarrollo) ---
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta_data = os.path.abspath(os.path.join(directorio_actual, '..', '..', 'Data'))
        ruta_archivo_db = os.path.join(ruta_carpeta_data, 'metricgoal.duckdb')

        if not os.path.exists(ruta_carpeta_data):
            os.makedirs(ruta_carpeta_data)
        
        try:
            return duckdb.connect(ruta_archivo_db)
        except Exception as e:
            print(f"❌ Error al conectar localmente: {e}")
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