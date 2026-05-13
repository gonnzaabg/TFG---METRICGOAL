import os
import sys

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_raiz)

from Modelo.database import obtener_conexion


def ver_correos():
    con = obtener_conexion()
    if not con:
        print("❌ No se pudo conectar a la base de datos.")
        return

    try:
        consulta = """
            SELECT
                id_cuerpo_tecnico,
                nombre,
                apellidos,
                email
            FROM cuerpo_tecnico
            ORDER BY id_cuerpo_tecnico
        """
        resultados = con.execute(consulta).fetchall()

        if not resultados:
            print("No hay correos registrados.")
            return

        print("\n📧 Correos registrados:\n")
        for fila in resultados:
            id_ct, nombre, apellidos, email = fila
            print(f"{id_ct} | {nombre} {apellidos} | {email}")

    except Exception as e:
        print(f"❌ Error al obtener correos: {e}")
    finally:
        con.close()


if __name__ == "__main__":
    ver_correos()