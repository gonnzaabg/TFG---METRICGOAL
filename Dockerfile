FROM python:3.10-slim

WORKDIR /app

# 1. Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiamos todo el contenido
COPY . .

# 3. Path para que Python encuentre los controladores y modelos
ENV PYTHONPATH="/app:/app/METRICGOAL/Servidor"

EXPOSE 8000

# 4. EL COMANDO CON LA M MAYÚSCULA (tal cual está en GitHub)
CMD ["uvicorn", "METRICGOAL.Servidor.Main:app", "--host", "0.0.0.0", "--port", "8000"]