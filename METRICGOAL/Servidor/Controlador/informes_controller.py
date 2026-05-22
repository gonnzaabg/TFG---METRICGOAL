import json
from Modelo.database import ejecutar_consulta


def guardar_informe_logic(id_equipo, informe):
    """
    Guarda un informe comparativo en la base de datos asociado a un equipo.
    Extrae el nombre del canterano y profesional del objeto datos para
    facilitar búsquedas rápidas, y serializa el objeto completo en datos_json.
    """
    try:
        query = """
            INSERT INTO informes (id_equipo, fecha, temporada, canterano, profesional, datos_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """
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
    """
    Devuelve los últimos 20 informes guardados de un equipo.
    Deserializa el JSON de cada informe y aplana los datos para que
    el frontend pueda acceder directamente a canterano, profesional y labels.
    """
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
                    "canterano": datos.get("canterano"),
                    "profesional": datos.get("profesional"),
                    "labels": datos.get("labels"),
                })
            return informes
        return []
    except Exception as e:
        print(f"Error listando informes: {e}")
        return []


def borrar_informe_logic(id_informe, id_equipo):
    """
    Elimina un informe de la base de datos.
    Usa el id_equipo como medida de seguridad para evitar
    que un usuario borre informes de otro equipo.
    """
    try:
        query = "DELETE FROM informes WHERE id_informe = ? AND id_equipo = ?"
        ejecutar_consulta(query, (id_informe, id_equipo))
        return {"status": "success"}
    except Exception as e:
        print(f"Error borrando informe: {e}")
        return {"status": "error", "message": str(e)}