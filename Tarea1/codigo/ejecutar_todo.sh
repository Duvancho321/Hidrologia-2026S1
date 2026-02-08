#!/bin/bash
# Script para ejecutar todo el flujo de trabajo

source ~/miniforge3/etc/profile.d/conda.sh
conda activate hidrologia

echo "========================================="
echo "TAREA 1: MODELO HIDROLÓGICO DE DOS TANQUES"
echo "========================================="

echo -e "\n[1/4] Explorando y seleccionando cuenca..."
python 01_explorar_cuencas.py

echo -e "\n[2/4] Preparando datos..."
python 02_preparar_datos.py

echo -e "\n[3/6] Calibrando modelo (esto puede tomar varios minutos)..."
python 03_calibrar.py

echo -e "\n[4/6] Análisis básico..."
python 04_analisis.py

echo -e "\n[5/6] Análisis avanzado (KGE, sensibilidad, visualizaciones)..."
python 05_analisis_avanzado.py

echo -e "\n[6/6] Comparación de fuentes de precipitación..."
python 06_comparar_fuentes.py

echo -e "\n========================================="
echo "✓ COMPLETADO!"
echo "========================================="
echo ""
echo "📊 Resultados generados:"
echo "  Figuras:"
echo "    - exploracion_cuencas.png"
echo "    - series_tiempo.png"
echo "    - calibracion.png"
echo "    - validacion.png"
echo "    - comparacion_precip.png"
echo "    - analisis_avanzado.png (NUEVO: 9 subplots)"
echo "    - comparacion_fuentes_detallada.png (NUEVO)"
echo ""
echo "  Datos:"
echo "    - parametros_optimos.csv"
echo "    - metricas_completas.csv (NUEVO: NSE, KGE, r, α, β, RMSE, PBIAS)"
echo "    - sensibilidad.csv (NUEVO)"
echo "    - comparacion_fuentes.csv (NUEVO)"
echo ""
echo "📁 Ubicación:"
echo "  - Figuras: ../figuras/"
echo "  - Datos: ../datos/"
echo ""
echo "========================================="
