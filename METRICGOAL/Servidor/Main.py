from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse 
import os

# ¡Importamos el controlador!
from Controlador.auth_controller import verificar_credenciales

# 1. CREAR LA INSTANCIA DE LA APP (Fundamental que esté aquí arriba)
app = FastAPI()

# 2. CONFIGURAR CORS (Para que no te dé problemas de permisos desde el navegador)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 3. CONFIGURAR RUTAS DE CARPETAS
# Buscamos la carpeta 'Vista' que está en el mismo nivel que este Main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISTA_DIR = os.path.join(BASE_DIR, "Vista")

# 4. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# Ahora 'app' ya existe, así que no dará error
app.mount("/static", StaticFiles(directory=VISTA_DIR), name="static")

# --- RUTAS PARA LOS ARCHIVOS HTML ---

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(VISTA_DIR, "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    with open(os.path.join(VISTA_DIR, "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/informes", response_class=HTMLResponse)
async def read_informes():
    with open(os.path.join(VISTA_DIR, "informes.html"), "r", encoding="utf-8") as f:
        return f.read()

# --- LÓGICA DE LA API (LOGIN) ---

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
                "message": f"Bienvenido, {datos_usuario['nombre']}",
                "nombre": datos_usuario['nombre'],
                "club": datos_usuario['club'],
                "equipo": datos_usuario['equipo']
            }
        else:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"Error en el login: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    import uvicorn
    # Render usa la variable PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)