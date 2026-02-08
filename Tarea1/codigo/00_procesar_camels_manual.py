"""Procesar datos CAMELS descargados manualmente - Solo cuenca 11180500

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Extracción y procesamiento de datos CAMELS desde ZIP.
"""
from pandas import read_csv, DataFrame, to_datetime
from pathlib import Path
from zipfile import ZipFile

DATOS = Path(__file__).parent.parent / 'datos'
# MODIFICAR esta ruta según donde descargaste CAMELS
CAMELS_ZIP = Path.home() / 'Downloads' / 'basin_timeseries_v1p2_modelOutput_daymet.zip'

# Verificar existencia
if not CAMELS_ZIP.exists():
    print(f"❌ No se encontró: {CAMELS_ZIP}")
    print("\n📝 INSTRUCCIONES:")
    print("1. Descarga desde: https://zenodo.org/records/15529996")
    print("2. Archivo: basin_timeseries_v1p2_modelOutput_daymet.zip")
    print(f"3. Colócalo en: {CAMELS_ZIP}")
    print("4. O modifica línea 7 de este script con tu ruta")
    exit(1)

# Cargar ID de cuenca seleccionada
cuenca = read_csv(DATOS / 'cuenca_seleccionada.csv').iloc[0]
gauge_id = str(int(cuenca['gauge_id']))

print(f"🎯 Procesando cuenca: {gauge_id}")
print(f"📦 Leyendo ZIP: {CAMELS_ZIP.name} ({CAMELS_ZIP.stat().st_size/1024/1024:.1f} MB)")

# Extraer datos de la cuenca del ZIP (sin descomprimir todo)
with ZipFile(CAMELS_ZIP, 'r') as zf:
    # Buscar archivos de nuestra cuenca
    prefix = gauge_id[:2]
    archivos = [f for f in zf.namelist()
                if f'{prefix}/{gauge_id}_' in f and f.endswith('.txt')]

    if not archivos:
        print(f"❌ No se encontraron archivos para cuenca {gauge_id}")
        print(f"   Buscando patrón: {prefix}/{gauge_id}_*.txt")
        print(f"\n   Archivos disponibles en {prefix}/:")
        print([f for f in zf.namelist() if f.startswith(f'{prefix}/')])
        exit(1)

    print(f"✓ Encontrados {len(archivos)} archivos")

    # Procesar cada archivo
    datos = {}
    for archivo in archivos:
        print(f"  📄 {Path(archivo).name[:50]}...")
        with zf.open(archivo) as f:
            df = read_csv(f, sep=r'\s+', comment='#')

            # Crear columna fecha
            df['fecha'] = (to_datetime(df[['Year', 'Mnth', 'Day']]) if 'Year' in df.columns
                          else to_datetime({k:df[v] for k,v in
                              {'year':'YR','month':'MNTH','day':'DY'}.items()}))

            # Identificar fuente
            fuente = ('daymet' if 'daymet' in archivo.lower() else
                     'maurer' if 'maurer' in archivo.lower() else
                     'nldas' if 'nldas' in archivo.lower() else 'obs')
            datos[fuente] = df

# Combinar datos
print("\n🔄 Combinando datos...")
df_base = datos[list(datos.keys())[0]][['fecha']].copy()

for fuente, df in datos.items():
    # Precipitación
    col_p = next((c for c in df.columns if 'prcp' in c.lower()), None)
    if col_p:
        df_base[f'prcp_{fuente}'] = df[col_p].values
        print(f"  ✓ prcp_{fuente}: {df[col_p].mean():.2f} mm/d")

    # Temperatura
    col_t = next((c for c in df.columns if 'tmax' in c.lower() or 'tmean' in c.lower()), None)
    if col_t:
        df_base[f'temp_{fuente}'] = df[col_t].values

    # Caudal observado
    col_q = next((c for c in df.columns if 'runoff' in c.lower() or c.lower() in ['q','qobs']), None)
    if col_q and 'qobs' not in df_base.columns:
        df_base['qobs'] = df[col_q].values
        print(f"  ✓ qobs: {df[col_q].mean():.3f} mm/d")

# Separar forzamiento y caudal
cols_forz = ['fecha'] + [c for c in df_base.columns if 'prcp' in c or 'temp' in c]
forzamiento = df_base[cols_forz].dropna()
caudal = df_base[['fecha', 'qobs']].dropna() if 'qobs' in df_base.columns else None

# Guardar en parquet (eficiente) y CSV (compatibilidad)
print("\n💾 Guardando datos...")
forzamiento.to_parquet(DATOS / 'forzamiento.parquet', compression='snappy')
forzamiento.to_csv(DATOS / 'forzamiento.csv', index=False)
print(f"  ✓ forzamiento.parquet: {len(forzamiento)} días, {forzamiento.memory_usage().sum()/1024:.1f} KB")

if caudal is not None:
    caudal.to_parquet(DATOS / 'caudal.parquet', compression='snappy')
    caudal.to_csv(DATOS / 'caudal.csv', index=False)
    print(f"  ✓ caudal.parquet: {len(caudal)} días, {caudal.memory_usage().sum()/1024:.1f} KB")

# Estadísticas
print(f"\n📊 Período: {forzamiento['fecha'].min().date()} a {forzamiento['fecha'].max().date()}")
print(f"   Días totales: {len(forzamiento)}")
print(f"\n🎉 ¡Listo! Ahora ejecuta:")
print(f"   cd codigo/")
print(f"   ./ejecutar_todo.sh")
print(f"\n   O solo la calibración:")
print(f"   python 03_calibrar.py")
