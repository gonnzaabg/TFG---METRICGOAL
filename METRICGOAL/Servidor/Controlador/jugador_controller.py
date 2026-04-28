from Modelo.Canterano import Canterano
from Modelo.database import ejecutar_consulta

# Le cambiamos el nombre a la función para que sea único
def gestionar_registro_canterano(datos_validados, id_equipo):
    try:
        Canterano.guardar_en_db(
            id_equipo,
            datos_validados.nombre, 
            datos_validados.apellidos, 
            datos_validados.edad, 
            datos_validados.posicion
        )
        return {"status": "success"}
    except Exception as e:
        print(f"Error en controlador: {e}")
        return {"status": "error", "message": str(e)}

def listar_jugadores_logic(id_equipo):
    # Aseguramos creación por si acaso es la primera vez que se consulta
    ejecutar_consulta("""
        CREATE TABLE IF NOT EXISTS Jugadores (
            nombre TEXT,
            apellido TEXT,
            edad INTEGER,
            posicion TEXT
        )
    """)
    
    query = "SELECT nombre, apellidos, posicion FROM jugadores WHERE id_equipo = ?"
    df = ejecutar_consulta(query, (id_equipo,))
    
    if df is not None and not df.empty:
        return df.to_dict(orient='records')
    return []       