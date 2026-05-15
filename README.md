# MetricGoal 🏆

Aplicación web multiplataforma para el análisis y comparación de jugadores de cantera con profesionales de élite.

## ¿Qué es MetricGoal?

MetricGoal permite a los cuerpos técnicos de clubes de fútbol registrar las estadísticas de sus canteranos y compararlas visualmente con jugadores profesionales de las 5 grandes ligas, generando informes exportables en PDF.

## Funcionalidades principales

- Gestión de jugadores por posición (CRUD)
- Registro de estadísticas por temporada
- Comparativa visual con jugadores profesionales (gráfico radar y barras)
- Generación y exportación de informes en PDF
- Visualización de informes guardados dentro de la app
- Estadísticas globales del equipo

## Tecnologías utilizadas

- **Backend:** Python, FastAPI, Uvicorn, Pandas, DuckDB
- **Frontend:** HTML5, CSS3, JavaScript, Plotly.js, Chart.js, jsPDF
- **Base de datos:** DuckDB + MotherDuck (cloud)
- **Despliegue:** Render
- **Escritorio:** Electron (.exe)

## Acceso web

https://tfg-metricgoal-bueno.onrender.com

## Instalación local

1. Clona el repositorio:
   git clone https://github.com/gonnzaabg/TFG---METRICGOAL.git

2. Crea un entorno virtual e instala dependencias:
   cd TFG---METRICGOAL
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Configura la variable de entorno:
   MOTHERDUCK_TOKEN=tu_token_aqui

4. Arranca el servidor:
   cd METRICGOAL/Servidor
   python main.py

5. Accede desde el navegador a:
   http://localhost:8000

## Autor

Gonzalo Bouso Gómez — CES Cristo Rey — DAM 2025/2026
