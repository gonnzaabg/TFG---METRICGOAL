import pandas as pd
from Modelo.database import ejecutar_consulta

def mostrar_y_exportar_tablas():
    # --- CONFIGURACIÓN DE PANDAS ---
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    # 1. Ejecutamos las consultas para obtener los datos
    tabla_club = ejecutar_consulta("SELECT * FROM club")
    tabla_equipo = ejecutar_consulta("SELECT * FROM equipo")
    tabla_tecnico = ejecutar_consulta("SELECT * FROM cuerpo_tecnico")

    # 2. Añadimos la columna identificadora para el CSV
    if not tabla_club.empty: tabla_club['tabla_origen'] = 'CLUB'
    if not tabla_equipo.empty: tabla_equipo['tabla_origen'] = 'EQUIPO'
    if not tabla_tecnico.empty: tabla_tecnico['tabla_origen'] = 'CUERPO_TECNICO'

    # --- MOSTRAR POR CONSOLA ---
    print("\n" + "="*40)
    print("🏢 TABLA: CLUB")
    print("="*40)
    print(tabla_club)

    print("\n" + "="*40)
    print("⚽ TABLA: EQUIPOS")
    print("="*40)
    print(tabla_equipo)

    print("\n" + "="*40)
    print("📋 TABLA: CUERPO TÉCNICO")
    print("="*40)
    
    if not tabla_tecnico.empty:
        for index, fila in tabla_tecnico.iterrows():
            email = fila.get('email', 'Sin correo')
            id_equipo = fila.get('id_equipo')
            
            nombre_equipo = "Desconocido"
            nombre_club = "Desconocido"
            
            # Buscar el equipo usando el id_equipo
            if pd.notna(id_equipo) and not tabla_equipo.empty:
                # Comprueba si la clave primaria en la tabla equipo se llama 'id' o 'id_equipo'
                pk_equipo = 'id_equipo' if 'id_equipo' in tabla_equipo.columns else 'id'
                equipo_fila = tabla_equipo[tabla_equipo[pk_equipo] == id_equipo]
                
                if not equipo_fila.empty:
                    # ✅ AQUÍ ESTÁ EL CAMBIO: Usamos 'categoria' en lugar de 'nombre'
                    nombre_equipo = equipo_fila.iloc[0].get('categoria', 'Desconocido')
                    id_club = equipo_fila.iloc[0].get('id_club')
                    
                    # Buscar el club usando el id_club del equipo
                    if pd.notna(id_club) and not tabla_club.empty:
                        # Comprueba si la clave primaria en la tabla club se llama 'id' o 'id_club'
                        pk_club = 'id_club' if 'id_club' in tabla_club.columns else 'id'
                        club_fila = tabla_club[tabla_club[pk_club] == id_club]
                        
                        if not club_fila.empty:
                            nombre_club = club_fila.iloc[0].get('nombre', 'Desconocido')

            # Imprimimos con el formato exacto que pediste
            print(f"{email} - {nombre_club} - {nombre_equipo}")
    else:
        print("La tabla no tiene registros.")
    print("\n")

    # --- EXPORTAR A CSV ---
    print("="*40)
    print("💾 EXPORTANDO A CSV...")
    print("="*40)
    
    # Concatenamos todas las tablas en una sola
    df_final = pd.concat([tabla_club, tabla_equipo, tabla_tecnico], ignore_index=True, sort=False)

    # Guardamos el archivo
    nombre_archivo = 'metricgoal.csv'
    df_final.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep=';')
    
    print(f"✅ ¡Éxito! Se ha creado el archivo: {nombre_archivo}\n")

if __name__ == "__main__":
    mostrar_y_exportar_tablas()