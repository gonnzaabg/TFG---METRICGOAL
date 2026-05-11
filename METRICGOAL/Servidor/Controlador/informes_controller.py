import json
from Modelo.database import ejecutar_consulta


def guardar_informe_logic(id_equipo, informe):
    try:
        query = """
            INSERT INTO informes (id_equipo, fecha, temporada, canterano, profesional, datos_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        # canterano y profesional son strings (nombres) para búsquedas rápidas en BD
        # datos contiene el objeto completo {canterano:{nombre,valores}, profesional:{nombre,valores}, labels:[]}
        canterano_nombre = informe['datos'].get('canterano', {}).get('nombre', informe.get('canterano', ''))
        profesional_nombre = informe['datos'].get('profesional', {}).get('nombre', informe.get('profesional', ''))

        params = (
            id_equipo,
            informe['fecha'],
            informe['temporada'],
            canterano_nombre,
            profesional_nombre,
            json.dumps(informe['datos'])
        )
        print(f"🔍 Intentando guardar informe: id_equipo={id_equipo}, canterano={canterano_nombre}")
        resultado = ejecutar_consulta(query, params)
        print(f"🔍 Resultado del INSERT: {resultado}")

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
                datos = json.loads(row['datos_json'])
                informes.append({
                    "id": row['id_informe'],
                    "fecha": row['fecha'],
                    "temporada": row['temporada'],
                    # El front accede a inf.canterano.nombre, inf.profesional.nombre, inf.labels
                    # así que aplanamos datos directamente aquí:
                    "canterano": datos.get("canterano"),    # {nombre, valores}
                    "profesional": datos.get("profesional"), # {nombre, valores}
                    "labels": datos.get("labels"),           # ["Goles", "Asistencias", ...]
                })
            return informes
        return []
    except Exception as e:
        print(f"Error listando informes: {e}")
        return []


def borrar_informe_logic(id_informe, id_equipo):
    try:
        query = "DELETE FROM informes WHERE id_informe = ? AND id_equipo = ?"
        ejecutar_consulta(query, (id_informe, id_equipo))
        return {"status": "success"}
    except Exception as e:
        print(f"Error borrando informe: {e}")
        return {"status": "error", "message": str(e)}