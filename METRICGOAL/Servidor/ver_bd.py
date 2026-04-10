from Modelo.database import ejecutar_consulta

def mostrar_tablas():
    print("\n" + "="*40)
    print("🏢 TABLA: CLUB")
    print("="*40)
    # Ejecutamos la consulta y pandas nos devuelve una tabla formateada
    tabla_club = ejecutar_consulta("SELECT * FROM club")
    print(tabla_club)

    print("\n" + "="*40)
    print("⚽ TABLA: EQUIPOS")
    print("="*40)
    tabla_equipo = ejecutar_consulta("SELECT * FROM equipo")
    print(tabla_equipo)

    print("\n" + "="*40)
    print("📋 TABLA: CUERPO TÉCNICO")
    print("="*40)
    tabla_tecnico = ejecutar_consulta("SELECT * FROM cuerpo_tecnico")
    print(tabla_tecnico)
    print("\n")

if __name__ == "__main__":
    mostrar_tablas()