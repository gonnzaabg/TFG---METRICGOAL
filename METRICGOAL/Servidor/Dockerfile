# 1. Usamos una imagen de Python ligera
FROM python:3.10-slim

# 2. Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos todo tu código (incluyendo la carpeta Controlador y el archivo .duckdb)
COPY . .

# 5. Exponemos el puerto 8000 que es el que usa tu código
EXPOSE 8000

# 6. Comando para arrancar la aplicación
# Usamos el comando directo de uvicorn para que sea más estable en producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]