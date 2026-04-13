import pandas as pd
from Modelo.database import obtener_conexion
import os

def importar_clubes_desde_csv():

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.abspath(os.path.join(directorio_actual, '..', 'BD_METRICGOAL.csv'))
    
    if not os.path.exists(ruta_csv):
        print(f"❌ No se encuentra el archivo CSV en: {ruta_csv}")
        return

    print("📊 Leyendo el archivo CSV...")
    
    # 2. Leer el CSV con Pandas
    df = pd.read_csv(ruta_csv)
    
    # 3. Extraer los nombres únicos de la columna 'team'
    # Usamos dropna() por si hay alguna fila vacía
    clubes_unicos = df['team'].dropna().unique()
    
    print(f"✅ Se han encontrado {len(clubes_unicos)} clubes únicos. Conectando a la base de datos...")

    # 4. Conectar a DuckDB
    con = obtener_conexion()
    if not con:
        return

    # 5. Insertar los clubes en la base de datos
    # Empezamos el ID en 2, porque el ID 1 ya lo ocupamos con 'MetricGoal F.C.'
    id_actual = 2
    clubes_insertados = 0
    
    try:
        for nombre_club in clubes_unicos:
            # Limpiamos los espacios en blanco por si acaso
            nombre_limpio = nombre_club.strip()
            
            # Insertamos en la tabla club
            con.execute("INSERT OR IGNORE INTO club (id_club, nombre) VALUES (?, ?)", (id_actual, nombre_limpio))
            id_actual += 1
            clubes_insertados += 1
            
        print(f"🎉 ¡Éxito! Se han guardado {clubes_insertados} clubes profesionales en la base de datos.")
        
    except Exception as e:
        print(f"❌ Error durante la inserción: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    importar_clubes_desde_csv()