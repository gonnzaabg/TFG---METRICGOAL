import json
from Modelo.database import ejecutar_consulta


def guardar_informe_logic(id_equipo, informe):
    try:
        query = """
            INSERT INTO informes (id_equipo, fecha, temporada, canterano, profesional, datos_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            id_equipo,
            informe['fecha'],
            informe['temporada'],
            informe['canterano'],
            informe['profesional'],
            json.dumps(informe['datos'])
        )
        print(f"🔍 Intentando guardar informe: id_equipo={id_equipo}, canterano={informe['canterano']}")
        resultado = ejecutar_consulta(query, params)
        print(f"🔍 Resultado del INSERT: {resultado}")

        # Verificamos que realmente se guardó
        check = ejecutar_consulta("SELECT COUNT(*) as total FROM informes WHERE id_equipo = ?", (id_equipo,))
        print(f"🔍 Informes en BD tras insertar: {check}")

        return {"status": "success"}
    except Exception as e:
        print(f"Error guardando informe: {e}")
        return {"status": "error", "message": str(e)}


def listar_informes_logic(id_equipo):
    try:
        query = """
            SELECT id_informe, fecha, temporada, canterano, profesional, datos_json
            FROM informes
            WHERE id_equipo = ?
            ORDER BY id_informe DESC
            LIMIT 20
        """
        df = ejecutar_consulta(query, (id_equipo,))

        if df is not None and not df.empty:
            informes = []
            for _, row in df.iterrows():
                informes.append({
                    "id": row['id_informe'],
                    "fecha": row['fecha'],
                    "temporada": row['temporada'],
                    "canterano": row['canterano'],
                    "profesional": row['profesional'],
                    "datos": json.loads(row['datos_json'])
                })
            return informes
        return []
    except Exception as e:
        print(f"Error listando informes: {e}")
        return []


def borrar_informe_logic(id_informe, id_equipo):
    try:
        # El id_equipo evita que un usuario borre informes de otro
        query = "DELETE FROM informes WHERE id_informe = ? AND id_equipo = ?"
        ejecutar_consulta(query, (id_informe, id_equipo))
        return {"status": "success"}
    except Exception as e:
        print(f"Error borrando informe: {e}")
        return {"status": "error", "message": str(e)}