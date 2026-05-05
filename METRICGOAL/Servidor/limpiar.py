import os
from Modelo.database import ejecutar_consulta

def limpiar_y_reimportar():
    # 1. Ruta del CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Ajusta si está en Scripts o en Servidor según tu estructura real
    ruta_csv = os.path.normpath(os.path.join(base_dir, "Scripts", "BD_METRICGOAL - Hoja 1.csv"))

    if not os.path.exists(ruta_csv):
        print(f"❌ No se encuentra el CSV en: {ruta_csv}")
        return

    try:
        print("--- Iniciando proceso de limpieza ---")
        
        # 2. BORRAR LA TABLA MAL IMPORTADA
        ejecutar_consulta("DROP TABLE IF EXISTS profesionales")
        print("🗑️ Tabla antigua borrada.")

        # 3. IMPORTACIÓN FORZANDO EL FORMATO CORRECTO
        # Usamos 'read_csv' con parámetros manuales para que no se líe con los puntos
        sql_importar = f"""
            CREATE TABLE profesionales AS 
            SELECT * FROM read_csv('{ruta_csv}', 
                header=True, 
                delim=',', 
                quote='"',
                ignore_errors=True)
        """
        ejecutar_consulta(sql_importar)
        
        # 4. VERIFICACIÓN FINAL
        df_verificar = ejecutar_consulta("SELECT COUNT(*) as total FROM profesionales")
        total = df_verificar['total'][0]
        
        print(f"✅ ¡Ahora sí! {total} jugadores cargados correctamente.")
        
        if total != 662:
            print("⚠️ Nota: El número sigue sin ser 662. Revisa si el CSV tiene filas extra al final.")

    except Exception as e:
        print(f"❌ Error en el proceso: {e}")

if __name__ == "__main__":
    limpiar_y_reimportar()