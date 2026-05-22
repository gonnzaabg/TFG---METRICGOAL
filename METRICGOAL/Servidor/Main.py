from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

from Controlador.auth_controller import verificar_credenciales
from Controlador.jugador_controller import (
    gestionar_registro_canterano,
    listar_jugadores_logic,
    gestionar_registro_stats,
    obtener_stats_jugador_temporada,
    eliminar_jugador_logic,
    obtener_profesionales_busqueda,
    obtener_datos_comparativa,
    obtener_stats_destacados,
    obtener_stats_equipo
)
from Controlador.informes_controller import guardar_informe_logic, listar_informes_logic, borrar_informe_logic
from inicializar_bd import preparar_base_de_datos


# ── Inicialización de la app ──────────────────────────────────────────────────

app = FastAPI()
preparar_base_de_datos()


# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ── Rutas de archivos estáticos ───────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISTA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Cliente", "Vista"))
STATIC_DIR = os.path.join(VISTA_DIR, "static")

print(f"DEBUG: Buscando HTML en: {VISTA_DIR}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ── Modelos Pydantic ──────────────────────────────────────────────────────────

class LoginData(BaseModel):
    email: str
    password: str

class JugadorData(BaseModel):
    nombre: str
    apellidos: str
    edad: int
    posicion: str

class EstadisticasData(BaseModel):
    temporada: str
    goles: int
    asistencias: int
    tarj_amarillas: int
    tarj_rojas: int
    partidos_jugados: int
    minutos_jugados: int
    pases_clave: int

class InformeData(BaseModel):
    fecha: str
    temporada: str
    canterano: str
    profesional: str
    datos: dict


# ── Rutas HTML ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Sirve la página de login."""
    path = os.path.join(VISTA_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    """Sirve la página principal del equipo."""
    path = os.path.join(VISTA_DIR, "dashboard.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/informes", response_class=HTMLResponse)
async def read_informes():
    """Sirve la página de informes guardados."""
    path = os.path.join(VISTA_DIR, "informes.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/comparar_jugadores", response_class=HTMLResponse)
async def read_comparar():
    """Sirve la página de comparación de jugadores."""
    path = os.path.join(VISTA_DIR, "comparar_jugadores.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── Endpoints de autenticación ────────────────────────────────────────────────

@app.post("/login")
async def login(data: LoginData):
    """Autentica al usuario y devuelve sus datos de sesión."""
    try:
        datos_usuario = verificar_credenciales(data.email, data.password)
        if datos_usuario:
            return {"status": "success", **datos_usuario}
        else:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"ERROR EN LOGIN: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Endpoints de jugadores ────────────────────────────────────────────────────

@app.get("/obtener_jugadores")
async def obtener_jugadores(id_equipo: int):
    """Devuelve la lista de jugadores de un equipo."""
    return listar_jugadores_logic(id_equipo)

@app.post("/registrar_jugador")
async def registrar_jugador(data: JugadorData, id_equipo: int):
    """Registra un nuevo jugador en el equipo."""
    return gestionar_registro_canterano(data, id_equipo)

@app.get("/obtener_stats")
async def obtener_stats(id_jugador: int, temporada: str):
    """Devuelve las estadísticas de un jugador en una temporada concreta."""
    return obtener_stats_jugador_temporada(id_jugador, temporada)

@app.post("/registrar_estadisticas")
async def registrar_estadisticas(data: EstadisticasData, id_jugador: int):
    """Guarda o actualiza las estadísticas de un jugador."""
    resultado = gestionar_registro_stats(data, id_jugador)
    if resultado.get("status") == "success":
        return resultado
    else:
        raise HTTPException(status_code=500, detail="No se pudieron guardar las estadísticas")

@app.delete("/eliminar_jugador/{id_jugador}")
async def eliminar_jugador(id_jugador: int):
    """Elimina un jugador y todas sus estadísticas asociadas."""
    resultado = eliminar_jugador_logic(id_jugador)
    if resultado.get("status") == "success":
        return resultado
    else:
        raise HTTPException(status_code=500, detail=resultado.get("message"))

@app.get("/stats_destacados")
async def stats_destacados(id_equipo: int):
    """Devuelve el máximo goleador y asistente del equipo."""
    return obtener_stats_destacados(id_equipo)

@app.get("/stats_equipo")
async def stats_equipo(id_equipo: int):
    """Devuelve las estadísticas globales acumuladas del equipo."""
    return obtener_stats_equipo(id_equipo)


# ── Endpoints de profesionales y comparativa ──────────────────────────────────

@app.get("/buscar_profesionales")
async def buscar_profesionales(nombre: str):
    """Busca jugadores profesionales por nombre."""
    return obtener_profesionales_busqueda(nombre)

@app.get("/api/comparar_jugadores")
async def api_comparar(id_canterano: int, nombre_profesional: str, temporada: str = "2025/26"):
    """Genera la comparativa entre un canterano y un jugador profesional."""
    try:
        datos = obtener_datos_comparativa(id_canterano, nombre_profesional, temporada)
        return datos
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return {"error": str(e)}


# ── Endpoints de informes ─────────────────────────────────────────────────────

@app.post("/guardar_informe")
async def guardar_informe(data: InformeData, id_equipo: int):
    """Guarda un informe comparativo asociado a un equipo."""
    return guardar_informe_logic(id_equipo, data.dict())

@app.get("/listar_informes")
async def listar_informes(id_equipo: int):
    """Devuelve todos los informes guardados de un equipo."""
    return listar_informes_logic(id_equipo)

@app.delete("/borrar_informe/{id_informe}")
async def borrar_informe(id_informe: int, id_equipo: int):
    """Elimina un informe de la base de datos."""
    return borrar_informe_logic(id_informe, id_equipo)


# ── Arranque local ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)