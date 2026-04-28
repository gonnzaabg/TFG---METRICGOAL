import random
from Modelo.database import obtener_conexion

def generar_cuerpo_tecnico():
    con = obtener_conexion()
    if not con:
        return

    print("👔 Contratando entrenadores (Nivel Experto: Máxima Variedad)...")

    # 45 Nombres internacionales
    nombres = [
        'Carlos', 'Miguel', 'David', 'John', 'Paul', 'Marco', 'Luca', 'Jean', 'Pierre', 'Hans', 'Thomas',
        'Alejandro', 'Javier', 'William', 'James', 'Alessandro', 'Giovanni', 'Antoine', 'Louis', 'Lukas', 'Felix', 'Hugo',
        'Diego', 'Daniel', 'Pablo', 'Sergio', 'Jorge', 'Mario', 'Luigi', 'Francesco', 'Antonio', 'Roberto', 
        'Michael', 'Robert', 'Richard', 'Joseph', 'Charles', 'Marcel', 'Luc', 'Julien', 'Klaus', 'Stefan', 'Dieter', 'Jürgen', 'Arthur'
    ]
    
    # 40 Apellidos internacionales
    apellidos = [
        'García', 'Martínez', 'Smith', 'Johnson', 'Rossi', 'Bianchi', 'Dupont', 'Martin', 'Müller', 'Weber',
        'López', 'Gómez', 'Williams', 'Brown', 'Romano', 'Colombo', 'Bernard', 'Richard', 'Schmidt', 'Wagner',
        'Fernández', 'Pérez', 'Rodríguez', 'Sánchez', 'Jones', 'Taylor', 'Davies', 'Evans', 'Ricci', 'Marino', 
        'Greco', 'Gallo', 'Petit', 'Roux', 'Leroy', 'Moreau', 'Becker', 'Hoffmann', 'Schäfer', 'Koch'
    ]

    try:
        # 1. Obtenemos todos los equipos (excepto el id=1, que es tu equipo de prueba)
        equipos = con.execute("SELECT id_equipo, id_club, categoria FROM equipo WHERE id_equipo > 1").fetchall()
        
        # 2. Buscamos el último ID de cuerpo_tecnico para no pisar a nadie
        max_id_query = con.execute("SELECT MAX(id_cuerpo_tecnico) FROM cuerpo_tecnico").fetchone()
        id_tecnico_actual = (max_id_query[0] or 0) + 1

        tecnicos_creados = 0

        # 3. Por cada equipo, creamos un Primer y Segundo Entrenador
        for equipo in equipos:
            id_equipo = equipo[0]
            
            for rol in ['Primer Entrenador', 'Segundo Entrenador']:
                nombre = random.choice(nombres)
                apellido = random.choice(apellidos)
                
                # Creamos un email único basado en el ID para evitar duplicados exactos
                email = f"{nombre[:3].lower()}{apellido.lower()}{id_tecnico_actual}@metricgoal.com"
                
                con.execute("""
                    INSERT INTO cuerpo_tecnico (id_cuerpo_tecnico, id_equipo, nombre, apellidos, email, password)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_tecnico_actual, id_equipo, nombre, f"{apellido} ({rol})", email, "metricg0al.1234"))
                
                id_tecnico_actual += 1
                tecnicos_creados += 1

        print(f"🎉 ¡Plantillas completadas! Se han generado {tecnicos_creados} técnicos súper variados en la base de datos.")

    except Exception as e:
        print(f"❌ Error al generar técnicos: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    generar_cuerpo_tecnico()