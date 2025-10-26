# Reportes CASA - Exploración de datos y desarrollo inicial

Este repositorio tiene el código fuente para la automatización de reportes de análisis de datos para el proyecto CASA.
Incluye scripts de consolidación de datos, análisis exploratorio y generación de tablas y gráficos preliminares
para apoyar el desarrollo de los reportes.

## Estructura del repositorio
- `data/`: Contiene los datos crudos y procesados utilizados en los análisis.
  - `data/reportes/`: Tablas y figuras generadas en formato XLSX y PNG.
  - `data/raw/`: Datos originales sin procesar, en formato XLSX.
    - `base.xlsx`: Archivo principal con los datos crudos.
    - `admitidos.xlsx`: Datos de estudiantes admitidos.
  - `data/Procesada/`: Datos limpios y transformados listos para análisis.
- `src/`: Scripts en Python para la limpieza, análisis y visualización de los datos
- `notebooks/`: Jupyter Notebooks con análisis exploratorio y visualizaciones interactivas.