import duckdb
import os
import pandas as pd

def obtener_conexion():
    token = os.getenv("MOTHERDUCK_TOKEN")
    
    if token:
        print("🚀 CONECTADO A MOTHERDUCK")
        try:
            con = duckdb.connect(f"md:metricgoal_md?motherduck_token={token}")
            con.execute("CREATE DATABASE IF NOT EXISTS metricgoal")
            con.execute("USE metricgoal")
            return con
        except Exception as e:
            print(f"❌ Error en MotherDuck: {e}")
            return None
    else:
        # --- MODO LOCAL ---
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
            resultado = con.execute(sql, params)
            
            if sql.strip().upper().startswith("SELECT"):
                return resultado.df()
            
            # Para INSERT, UPDATE, DELETE, CREATE: commit antes de cerrar
            con.commit()
            return True 
            
        except Exception as e:
            print(f"❌ Error en la consulta SQL: {e}")
            return None
        finally:
            con.close()
    return None