#!/bin/bash
# Descargar CAMELS desde Zenodo con link directo

DESTINO="$HOME/Downloads/basin_timeseries_v1p2_modelOutput_daymet.zip"
URL="https://zenodo.org/records/15529996/files/basin_timeseries_v1p2_modelOutput_daymet.zip?download=1"

echo "========================================="
echo "DESCARGANDO CAMELS DATASET"
echo "========================================="
echo "Tamaño: 4.2 GB"
echo "Destino: $DESTINO"
echo ""

# Verificar si ya existe
if [ -f "$DESTINO" ]; then
    echo "⚠️  El archivo ya existe en $DESTINO"
    echo "¿Quieres volver a descargar? (s/n)"
    read -r respuesta
    if [ "$respuesta" != "s" ]; then
        echo "Usando archivo existente."
        exit 0
    fi
fi

# Descargar con wget
if command -v wget &> /dev/null; then
    echo "Descargando con wget..."
    wget -c -O "$DESTINO" "$URL"
# O con curl
elif command -v curl &> /dev/null; then
    echo "Descargando con curl..."
    curl -L -o "$DESTINO" "$URL"
else
    echo "❌ No se encontró wget ni curl"
    echo "Instala wget: sudo apt install wget"
    echo "O descarga desde el navegador con el link arriba"
    exit 1
fi

# Verificar descarga
if [ -f "$DESTINO" ]; then
    TAMANIO=$(du -h "$DESTINO" | cut -f1)
    echo ""
    echo "========================================="
    echo "✓ DESCARGA COMPLETADA"
    echo "========================================="
    echo "Archivo: $DESTINO"
    echo "Tamaño: $TAMANIO"
    echo ""
    echo "Próximo paso:"
    echo "  cd ~/Documentos/UNAL/Hidrologia-2026S1/Tarea1/codigo"
    echo "  python 00_procesar_camels_manual.py"
else
    echo "❌ Error en la descarga"
    exit 1
fi
