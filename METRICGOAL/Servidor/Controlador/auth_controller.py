import pandas as pd
from Modelo.database import ejecutar_consulta

def verificar_credenciales(email: str, password: str):
    """
    Controlador encargado de gestionar el login.
    Devuelve un diccionario con los datos del usuario si hay éxito, o None si falla.
    """
    query = """
        SELECT 
            ct.nombre, 
            ct.apellidos, 
            e.categoria AS equipo, 
            c.nombre AS club
        FROM cuerpo_tecnico ct
        LEFT JOIN equipo e ON ct.id_equipo = e.id_equipo
        LEFT JOIN club c ON e.id_club = c.id_club
        WHERE ct.email = ? AND ct.contrasenia = ?
    """
    
    df = ejecutar_consulta(query, (email, password))
    
    if df is not None and not df.empty:
        usuario = df.iloc[0]
        
        # Procesamos la lógica de negocio aquí (limpiar datos, asignar valores por defecto)
        return {
            "nombre": str(usuario['nombre']),
            "club": str(usuario['club']) if pd.notna(usuario['club']) else "Sin Club",
            "equipo": str(usuario['equipo']) if pd.notna(usuario['equipo']) else "Sin Equipo"
        }
    
    return None # Si el login falla