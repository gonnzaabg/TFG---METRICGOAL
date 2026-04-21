FROM python:3.10-slim

WORKDIR /app

# 1. Copiar y subir librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiar todo el proyecto
COPY . .

# 3. Nos situamos exactamente donde está tu main.py
WORKDIR /app/METRICGOAL/Servidor

# 4. Forzamos que Python vea las carpetas Controlador, Modelo, etc.
ENV PYTHONPATH=/app/METRICGOAL/Servidor

EXPOSE 8000

# 5. Ejecución (como estamos dentro de Servidor, solo ponemos main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]