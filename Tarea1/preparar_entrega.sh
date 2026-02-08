#!/bin/bash
# Script para preparar archivo de entrega según especificaciones

# Configuración
APELLIDO="apellido"  # CAMBIAR
NOMBRE="nombre"      # CAMBIAR
ARCHIVO_SALIDA="${APELLIDO}_${NOMBRE}_tarea1.tar.gz"

echo "========================================="
echo "PREPARANDO ENTREGA TAREA 1"
echo "========================================="

# Crear estructura temporal
TEMP_DIR="temp_entrega"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR/{codigo,datos,figuras,informe}

# Copiar código
echo "[1/5] Copiando código..."
cp codigo/modelo.py $TEMP_DIR/codigo/
cp codigo/03_calibrar.py $TEMP_DIR/codigo/calibrar.py  # Renombrar según especificación
cp codigo/requirements.txt $TEMP_DIR/codigo/

# utils.py (crear si no existe)
if [ ! -f codigo/utils.py ]; then
    echo "# Funciones auxiliares" > $TEMP_DIR/codigo/utils.py
else
    cp codigo/utils.py $TEMP_DIR/codigo/
fi

# Copiar SOLO datos de la cuenca seleccionada (NO todo CAMELS)
echo "[2/5] Copiando datos..."
cp datos/forzamiento.csv $TEMP_DIR/datos/
cp datos/caudal.csv $TEMP_DIR/datos/
cp datos/cuenca_seleccionada.csv $TEMP_DIR/datos/atributos.csv

# Copiar figuras
echo "[3/5] Copiando figuras..."
[ -f figuras/series_tiempo.png ] && cp figuras/series_tiempo.png $TEMP_DIR/figuras/
[ -f figuras/calibracion.png ] && cp figuras/calibracion.png $TEMP_DIR/figuras/
[ -f figuras/validacion.png ] && cp figuras/validacion.png $TEMP_DIR/figuras/
[ -f figuras/comparacion_precip.png ] && cp figuras/comparacion_precip.png $TEMP_DIR/figuras/

# Copiar informe (debe existir informe.pdf)
echo "[4/5] Copiando informe..."
if [ -f informe/informe.pdf ]; then
    cp informe/informe.pdf $TEMP_DIR/informe/
    [ -f informe/informe.tex ] && cp informe/informe.tex $TEMP_DIR/informe/
else
    echo "ADVERTENCIA: informe/informe.pdf no encontrado!"
    echo "Crea el informe antes de generar la entrega"
fi

# Crear README.md
echo "[5/5] Creando README.md..."
cat > $TEMP_DIR/README.md << 'EOF'
# Tarea 1 - Modelo Hidrológico

## Autor: [Nombre Apellido]
## Cuenca seleccionada: [ID y nombre]

## Requisitos
pip install -r codigo/requirements.txt

## Ejecución
# Ejecutar calibración
python codigo/calibrar.py

## Resultados principales
- NSE calibración: X.XX
- NSE validación: X.XX

## Herramientas de IA utilizadas
- Claude Code (Anthropic): Asistencia en programación
  * Generación de código base del modelo
  * Implementación de optimización
  * Creación de visualizaciones
  * Todo el código fue revisado, entendido y modificado según necesidades
EOF

# Verificar tamaño
echo ""
echo "Verificando tamaño..."
TAMANIO=$(du -sh $TEMP_DIR | cut -f1)
echo "Tamaño total: $TAMANIO"

# Comprimir
echo ""
echo "Comprimiendo..."
tar -czf $ARCHIVO_SALIDA -C $TEMP_DIR .

# Limpiar
rm -rf $TEMP_DIR

# Verificar resultado
TAMANIO_FINAL=$(du -h $ARCHIVO_SALIDA | cut -f1)
echo ""
echo "========================================="
echo "ENTREGA LISTA!"
echo "========================================="
echo "Archivo: $ARCHIVO_SALIDA"
echo "Tamaño: $TAMANIO_FINAL"
echo ""

# Advertencia si es muy grande
TAMANIO_BYTES=$(stat -c%s $ARCHIVO_SALIDA)
if [ $TAMANIO_BYTES -gt 52428800 ]; then  # 50 MB
    echo "⚠️  ADVERTENCIA: Archivo mayor a 50 MB!"
    echo "   Verifica que NO incluiste todos los datos de CAMELS"
    echo "   Solo debes incluir datos de TU cuenca seleccionada"
else
    echo "✓ Tamaño correcto (< 50 MB)"
fi

echo ""
echo "Contenido del archivo:"
tar -tzf $ARCHIVO_SALIDA | head -20
echo "..."
echo ""
echo "Para verificar: tar -tzf $ARCHIVO_SALIDA"
echo "Para extraer: tar -xzf $ARCHIVO_SALIDA"
