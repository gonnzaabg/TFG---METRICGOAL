FROM python:3.10-slim

WORKDIR /app

# Instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos TODO el contenido (la carpeta METRICGOAL, el Dockerfile, etc.)
COPY . .

# Añadimos /app al path para que Python vea las carpetas internas como paquetes
ENV PYTHONPATH=/app

EXPOSE 8000

# El comando tiene que entrar en METRICGOAL, luego en Servidor y buscar Main
# Asegúrate de si es Main o main (en la foto no se ve, pero usa el que tengas)
CMD ["uvicorn", "METRICGOAL.Servidor.main:app", "--host", "0.0.0.0", "--port", "8000"]