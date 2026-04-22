from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse 
import os

# 1. IMPORTACIONES
from Controlador.auth_controller import verificar_credenciales

app = FastAPI()

# 2. CONFIGURAR CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 3. LOCALIZACIÓN DE LA CARPETA CLIENTE (Desde Servidor)
# BASE_DIR será: /app/METRICGOAL/Servidor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Subimos un nivel para salir de 'Servidor' y entramos en 'Cliente/Vista'
# La ruta resultante será: /app/METRICGOAL/Cliente/Vista
VISTA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Cliente", "Vista"))

# --- DEBUG PARA LOGS DE RENDER ---
print(f"DEBUG: Buscando HTML en: {VISTA_DIR}")

# 4. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
app.mount("/static", StaticFiles(directory=VISTA_DIR), name="static")

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
async def read_informes():
    path = os.path.join(VISTA_DIR, "comparar_jugadores.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()        

# --- LÓGICA DEL LOGIN ---
class LoginData(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    try:
        datos_usuario = verificar_credenciales(data.email, data.password)
        if datos_usuario:
            return {
                "status": "success", 
                "nombre": datos_usuario['nombre'],
                "club": datos_usuario['club'],
                "equipo": datos_usuario['equipo']
            }
        else:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)