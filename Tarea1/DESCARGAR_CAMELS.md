# 📥 Guía para Descargar Datos CAMELS

La cuenca seleccionada es: **11180500**

## Opción 1: Descarga desde Zenodo (Recomendado)

### Paso 1: Descargar archivo

Ve a: **https://zenodo.org/records/15529996**

Busca y descarga:
- **basin_timeseries_v1p2_modelOutput_daymet.zip** (~800 MB)

### Paso 2: Ubicar el archivo

Coloca el archivo descargado en:
```bash
~/camels_data/basin_timeseries_v1p2_modelOutput_daymet.zip
```

O en cualquier otra carpeta, solo recuerda la ruta.

### Paso 3: Procesar datos

```bash
conda activate hidrologia
cd ~/Documentos/UNAL/Hidrologia-2026S1/Tarea1/codigo

# Ejecutar procesamiento
python 00_procesar_camels_manual.py
```

---

## Opción 2: Descarga desde UCAR

### Paso 1: Ir al sitio oficial

Ve a: **https://ral.ucar.edu/solutions/products/camels**

### Paso 2: Descargar

Busca en "Download Data":
- Basin-scale meteorological forcing and streamflow observations

Descarga:
- **Daymet forcing and USGS streamflow** (model output format)

### Paso 3: Procesar

Igual que Opción 1, paso 3.

---

## Opción 3: Ya tengo los datos descargados

Si ya tienes CAMELS descargado en tu máquina:

```bash
# Editar 00_procesar_camels_manual.py línea ~10
CAMELS_ZIP = Path('/ruta/a/tu/basin_timeseries_v1p2_modelOutput_daymet.zip')

# Ejecutar
python 00_procesar_camels_manual.py
```

---

## ¿Qué hace el script de procesamiento?

1. Lee el ZIP de CAMELS (sin descomprimir todo)
2. Extrae SOLO los datos de la cuenca 11180500
3. Convierte a formato parquet (eficiente)
4. Guarda en `datos/forzamiento.parquet` y `datos/caudal.parquet`
5. También guarda CSV para compatibilidad

---

## Verificar que funcionó

Deberías ver:
```
✓ Datos guardados:
  - forzamiento.parquet: 12784 días, XX KB
  - caudal.parquet: 12784 días, XX KB

Columnas forzamiento: ['fecha', 'prcp_daymet', 'tmax_daymet', ...]
Columnas caudal: ['fecha', 'qobs']
```

Luego re-ejecuta la calibración:
```bash
./ejecutar_todo.sh
```

El NSE debería mejorar significativamente (> 0.5)
