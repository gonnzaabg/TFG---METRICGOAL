FROM python:3.10-slim

WORKDIR /app

# Instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido del repo
COPY . .

# Nos movemos a la carpeta donde está el código que se ejecuta
WORKDIR /app/METRICGOAL/Servidor

# Añadimos la ruta actual al PATH de Python
ENV PYTHONPATH=/app/METRICGOAL/Servidor

EXPOSE 8000

# Ahora que estamos DENTRO de Servidor, el módulo es simplemente "main" (o Main)
# IMPORTANTE: Usa "Main" si tu archivo empieza por mayúscula
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]