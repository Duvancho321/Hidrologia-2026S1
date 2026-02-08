#!/bin/bash
# Ejecutar solo calibración y análisis (asume que ya tienes datos procesados)

source ~/miniforge3/etc/profile.d/conda.sh
conda activate hidrologia

echo "========================================="
echo "ANÁLISIS RÁPIDO - MODELO DE DOS TANQUES"
echo "========================================="

# Verificar que existan los datos
if [ ! -f "../datos/forzamiento.csv" ]; then
    echo "❌ Error: No se encontró forzamiento.csv"
    echo "   Ejecuta primero: ./ejecutar_todo.sh"
    exit 1
fi

echo -e "\n[1/4] Calibrando modelo..."
python 03_calibrar.py

echo -e "\n[2/4] Análisis básico..."
python 04_analisis.py

echo -e "\n[3/4] Análisis avanzado (KGE, sensibilidad)..."
python 05_analisis_avanzado.py

echo -e "\n[4/4] Comparación de fuentes..."
python 06_comparar_fuentes.py

echo -e "\n========================================="
echo "✓ ANÁLISIS COMPLETADO"
echo "========================================="

# Mostrar métricas principales
if [ -f "../datos/metricas_completas.csv" ]; then
    echo -e "\n📊 MÉTRICAS PRINCIPALES:"
    echo ""
    python -c "
import pandas as pd
df = pd.read_csv('../datos/metricas_completas.csv', index_col=0)
print(df.to_string())
"
fi

echo -e "\n📁 Revisa:"
echo "  - ../figuras/analisis_avanzado.png"
echo "  - ../datos/metricas_completas.csv"
echo ""
