import pandas as pd
from Modelo.database import ejecutar_consulta

def verificar_credenciales(email, password_input): # <--- Aquí se llama password_input
    query = """
        SELECT 
            ct.nombre, 
            ct.id_equipo, 
            c.nombre AS club, 
            e.categoria AS equipo
        FROM cuerpo_tecnico ct
        JOIN equipo e ON ct.id_equipo = e.id_equipo
        JOIN club c ON e.id_club = c.id_club
        WHERE ct.email = ? AND ct.password = ?
    """
    
    # CAMBIO AQUÍ: Usamos password_input, que es como se llama tu variable
    df = ejecutar_consulta(query, (email, password_input)) 
    
    if df is not None and not df.empty:
        usuario = df.iloc[0]
        
        return {
            "status": "success",
            "nombre": str(usuario['nombre']),
            "id_equipo": int(usuario['id_equipo']),
            "club": str(usuario['club']),
            "equipo": str(usuario['equipo'])
        }
    
    return None