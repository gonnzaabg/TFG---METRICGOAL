from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse 
import os

# 1. IMPORTACIONES
from Controlador.auth_controller import verificar_credenciales
from Controlador.jugador_controller import gestionar_registro_canterano
from Controlador.jugador_controller import listar_jugadores_logic
from inicializar_bd import preparar_base_de_datos

app = FastAPI()

preparar_base_de_datos()

# 2. CONFIGURAR CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 3. LOCALIZACIÓN DE LA CARPETA CLIENTE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISTA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Cliente", "Vista"))

print(f"DEBUG: Buscando HTML en: {VISTA_DIR}")

# 4. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory=VISTA_DIR), name="static")

# --- MODELOS DE DATOS (Pydantic) ---

class LoginData(BaseModel):
    email: str
    password: str

# Esquema para recibir los datos del modal de añadir jugador
class JugadorData(BaseModel):
    nombre: str
    apellidos: str
    edad: int
    posicion: str

# --- RUTAS PARA LOS ARCHIVOS HTML ---

@app.get("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join(VISTA_DIR, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    path = os.path.join(VISTA_DIR, "dashboard.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/informes", response_class=HTMLResponse)
async def read_informes():
    path = os.path.join(VISTA_DIR, "informes.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/comparar_jugadores", response_class=HTMLResponse)
async def read_comparar():
    path = os.path.join(VISTA_DIR, "comparar_jugadores.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()  

@app.get("/obtener_jugadores")
async def obtener_jugadores(id_equipo: int): 
    return listar_jugadores_logic(id_equipo)         

# --- LÓGICA DE ENDPOINTS (API) ---

@app.post("/login")
async def login(data: LoginData):
    try:
        datos_usuario = verificar_credenciales(data.email, data.password)
        if datos_usuario:
            # Aquí 'datos_usuario' ya trae nombre, id_equipo, club y equipo
            return {
                "status": "success", 
                **datos_usuario # Esto desglosa el diccionario automáticamente
            }
        else:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"ERROR EN LOGIN: {e}") # Esto te ayudará a ver el fallo en la terminal
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/registrar_jugador")
async def registrar_jugador(data: JugadorData, id_equipo: int): # Recibe el ID de la URL
    # Ahora le pasamos 'id_equipo' a la lógica del controlador
    resultado = gestionar_registro_canterano(data, id_equipo) 
    return resultado

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)