from Modelo.database import obtener_conexion

def resetear_jugadores():
    con = obtener_conexion()
    if con:
        # Borramos la tabla vieja que no tiene id_equipo
        con.execute("DROP TABLE IF EXISTS jugadores")
        print("✅ Tabla 'jugadores' eliminada. Se recreará al iniciar el servidor.")
        con.close()

if __name__ == "__main__":
    resetear_jugadores()