"""Procesar datos CAMELS descargados - Versión corregida para estructura real

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.1"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-08]: Corrección para estructura real de CAMELS modelOutput.
"""
from pandas import read_csv, DataFrame, to_datetime
from pathlib import Path
from zipfile import ZipFile
from numpy import nan

DATOS = Path(__file__).parent.parent / 'datos'
CAMELS_ZIP = Path.home() / 'Downloads' / 'basin_timeseries_v1p2_modelOutput_daymet.zip'

if not CAMELS_ZIP.exists():
    print(f"❌ No se encontró: {CAMELS_ZIP}")
    exit(1)

# Cargar ID de cuenca
cuenca = read_csv(DATOS / 'cuenca_seleccionada.csv').iloc[0]
gauge_id = str(int(cuenca['gauge_id']))

print(f"🎯 Procesando cuenca: {gauge_id}")
print(f"📦 Leyendo ZIP: {CAMELS_ZIP.name} ({CAMELS_ZIP.stat().st_size/1024/1024:.1f} MB)")

# Extraer datos del ZIP
with ZipFile(CAMELS_ZIP, 'r') as zf:
    # Buscar archivos de la cuenca (estructura: model_output_daymet/model_output/flow_timeseries/{fuente}/{HUC2}/gauge_id_*_model_output.txt)
    prefix = gauge_id[:2]
    archivos = [f for f in zf.namelist() if gauge_id in f and 'model_output.txt' in f and not f.startswith('__MACOSX')]

    if not archivos:
        print(f"❌ No se encontraron archivos para cuenca {gauge_id}")
        exit(1)

    print(f"✓ Encontrados {len(archivos)} archivos")

    # Procesar cada archivo
    datos = {}
    for archivo in archivos:
        fuente = 'daymet' if 'daymet' in archivo else 'maurer' if 'maurer' in archivo else 'nldas' if 'nldas' in archivo else 'unknown'
        if fuente == 'unknown':
            continue

        print(f"  📄 Procesando {fuente.upper()}...")

        with zf.open(archivo) as f:
            # Leer archivo (formato VIC model output) - tiene header
            df = read_csv(f, sep=r'\s+', comment='#')

            # Crear fecha
            df['fecha'] = to_datetime(df[['YR', 'MNTH', 'DY']].rename(columns={'YR': 'year', 'MNTH': 'month', 'DY': 'day'}))
            datos[fuente] = df

# Combinar datos
print("\n🔄 Combinando datos...")
df_base = datos[list(datos.keys())[0]][['fecha']].copy()

for fuente, df in datos.items():
    # Precipitación
    df_base[f'prcp_{fuente}'] = df['PRCP'].values
    print(f"  ✓ prcp_{fuente}: {df['PRCP'].mean():.2f} mm/d")

    # PET (Evapotranspiración potencial)
    df_base[f'pet_{fuente}'] = df['PET'].values

    # Caudal observado
    if 'qobs' not in df_base.columns:
        df_base['qobs'] = df['OBS_RUN'].values
        print(f"  ✓ qobs: {df['OBS_RUN'].mean():.3f} mm/d")

# Separar forzamiento y caudal
cols_forz = ['fecha'] + [c for c in df_base.columns if 'prcp' in c or 'pet' in c]
forzamiento = df_base[cols_forz].dropna()
caudal = df_base[['fecha', 'qobs']].dropna()

# Guardar
print("\n💾 Guardando datos...")
forzamiento.to_parquet(DATOS / 'forzamiento.parquet', compression='snappy')
forzamiento.to_csv(DATOS / 'forzamiento.csv', index=False)
print(f"  ✓ forzamiento: {len(forzamiento)} días")

caudal.to_parquet(DATOS / 'caudal.parquet', compression='snappy')
caudal.to_csv(DATOS / 'caudal.csv', index=False)
print(f"  ✓ caudal: {len(caudal)} días")

# Estadísticas
print(f"\n📊 Período: {forzamiento['fecha'].min().date()} a {forzamiento['fecha'].max().date()}")
print(f"   Total días: {len(forzamiento)}")
print(f"\n🎉 ¡Listo! Datos reales de CAMELS procesados.")
print(f"\n   Siguiente paso:")
print(f"   python 03_calibrar.py")
