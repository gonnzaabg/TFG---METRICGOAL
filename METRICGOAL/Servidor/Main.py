from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ¡Importamos el controlador!
from Controlador.auth_controller import verificar_credenciales

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class LoginData(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    try:
        # 1. El controlador hace todo el trabajo sucio
        datos_usuario = verificar_credenciales(data.email, data.password)
        
        # 2. La ruta solo decide qué responder
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

# 👇 PEGADO A LA IZQUIERDA DEL TODO 👇
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)