FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Esto copiará todo lo que hay en la raíz (incluyendo la carpeta METRICGOAL)
COPY . .

EXPOSE 8000

# IMPORTANTE: Ahora la ruta al main incluye la carpeta METRICGOAL
CMD ["uvicorn", "METRICGOAL.Servidor.main:app", "--host", "0.0.0.0", "--port", "8000"]