from Modelo.database import obtener_conexion

def generar_equipos():
    con = obtener_conexion()
    if not con:
        return

    print("⚙️ Generando categorías (Filial, Juvenil A, Juvenil B) para los clubes...")

    try:
        # 1. Obtenemos todos los clubes, excepto el id=1 (nuestro MetricGoal FC)
        clubes = con.execute("SELECT id_club, nombre FROM club WHERE id_club > 1").fetchall()
        
        # 2. Averiguamos cuál es el último ID de equipo usado para no pisar datos
        max_id_query = con.execute("SELECT MAX(id_equipo) FROM equipo").fetchone()
        id_equipo_actual = (max_id_query[0] or 0) + 1

        categorias = ['Filial', 'Juvenil A', 'Juvenil B']
        equipos_creados = 0

        # 3. Por cada club, creamos los 3 equipos
        for club in clubes:
            id_club = club[0]
            
            for categoria in categorias:
                con.execute("""
                    INSERT INTO equipo (id_equipo, id_club, categoria) 
                    VALUES (?, ?, ?)
                """, (id_equipo_actual, id_club, categoria))
                
                id_equipo_actual += 1
                equipos_creados += 1

        print(f"🎉 ¡Misión cumplida! Se han creado {equipos_creados} equipos nuevos.")

    except Exception as e:
        print(f"❌ Error al crear los equipos: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    generar_equipos()