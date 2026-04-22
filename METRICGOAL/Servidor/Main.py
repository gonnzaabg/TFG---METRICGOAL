from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles # Importante
from fastapi.responses import HTMLResponse # Importante
import os

# ¡Importamos el controlador!
from Controlador.auth_controller import verificar_credenciales

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- 1. CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---
# Usamos la ruta completa que definiste en tu estructura de carpetas
app.mount("/static", StaticFiles(directory="METRICGOAL/Servidor/Vista"), name="static")

# --- 2. RUTAS PARA LOS ARCHIVOS HTML ---

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # El archivo de login
    with open("METRICGOAL/Servidor/Vista/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    with open("METRICGOAL/Servidor/Vista/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/informes", response_class=HTMLResponse)
async def read_informes():
    with open("METRICGOAL/Servidor/Vista/informes.html", "r", encoding="utf-8") as f:
        return f.read()
# --- 3. LÓGICA DE LA API (TU LOGIN) ---

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
    # En Render, el puerto lo da la variable de entorno $PORT, 
    # pero para local el 8000 está bien.
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)