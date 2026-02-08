"""Descargar y procesar datos CAMELS para cuenca seleccionada"""
import pandas as pd
import requests
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

DATOS = Path(__file__).parent.parent / 'datos'
CACHE = Path.home() / '.cache' / 'camels'
CACHE.mkdir(parents=True, exist_ok=True)

# URLs CAMELS
URLS = {
    'forzamiento': 'https://ral.ucar.edu/sites/default/files/public/product-tool/camels-catchment-attributes-and-meteorology-for-large-sample-studies-dataset-downloads/basin_timeseries_v1p2_modelOutput_daymet.zip',
    'caudal': 'https://ral.ucar.edu/sites/default/files/public/product-tool/camels-catchment-attributes-and-meteorology-for-large-sample-studies-dataset-downloads/basin_timeseries_v1p2_modelOutput_daymet.zip'
}

# Cargar cuenca seleccionada
cuenca = pd.read_csv(DATOS / 'cuenca_seleccionada.csv').iloc[0]
gauge_id = str(int(cuenca['gauge_id']))

print(f"Cuenca seleccionada: {gauge_id}")
print(f"Descargando datos CAMELS...")

def descargar_archivo(url, nombre):
    """Descargar archivo grande con progreso"""
    archivo_cache = CACHE / nombre
    if archivo_cache.exists():
        print(f"✓ Usando cache: {archivo_cache}")
        return archivo_cache

    print(f"Descargando {nombre} ({url[:50]}...)")
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))

        with open(archivo_cache, 'wb') as f:
            descargado = 0
            for chunk in r.iter_content(chunk_size=1024*1024):  # 1 MB chunks
                f.write(chunk)
                descargado += len(chunk)
                if total:
                    print(f"\r  {descargado/1024/1024:.1f}/{total/1024/1024:.1f} MB", end='')
        print("\n✓ Descargado")
        return archivo_cache
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def extraer_cuenca_zip(zip_path, gauge_id):
    """Extraer datos de una cuenca específica del ZIP"""
    datos_cuenca = {}

    with ZipFile(zip_path, 'r') as zf:
        # Buscar archivos de la cuenca
        prefix = gauge_id[:2]
        patron = f"{prefix}/{gauge_id}_"

        archivos = [f for f in zf.namelist() if patron in f and f.endswith('.txt')]
        print(f"Encontrados {len(archivos)} archivos para cuenca {gauge_id}")

        for archivo in archivos:
            print(f"  Procesando {Path(archivo).name}")
            with zf.open(archivo) as f:
                # Leer, saltando líneas de comentario
                df = pd.read_csv(f, sep=r'\s+', comment='#')

                # Crear fecha
                if 'Year' in df.columns:
                    df['fecha'] = pd.to_datetime(df[['Year', 'Mnth', 'Day']])
                elif 'YR' in df.columns:
                    df['fecha'] = pd.to_datetime(df[['YR', 'MNTH', 'DY']].rename(
                        columns={'YR':'Year','MNTH':'Mnth','DY':'Day'}))

                # Identificar tipo de dato
                if 'daymet' in archivo.lower():
                    tipo = 'daymet'
                elif 'maurer' in archivo.lower():
                    tipo = 'maurer'
                elif 'nldas' in archivo.lower():
                    tipo = 'nldas'
                else:
                    tipo = 'obs'

                datos_cuenca[tipo] = df

    return datos_cuenca

# Descargar ZIP principal
print("\n1. Descargando datos de forzamiento...")
zip_file = descargar_archivo(URLS['forzamiento'], 'camels_daymet.zip')

if zip_file and zip_file.exists():
    # Extraer datos de la cuenca
    print("\n2. Extrayendo datos de cuenca seleccionada...")
    datos = extraer_cuenca_zip(zip_file, gauge_id)

    if datos:
        # Combinar todas las fuentes
        print("\n3. Procesando datos...")

        # DataFrame base con fecha
        df_base = None

        for fuente, df in datos.items():
            if df_base is None:
                df_base = df[['fecha']].copy()

            # Renombrar columnas según fuente
            if 'prcp' in df.columns.str.lower().str.cat():
                col_p = [c for c in df.columns if 'prcp' in c.lower()][0]
                df_base[f'prcp_{fuente}'] = df[col_p].values

            if 'tmax' in df.columns.str.lower().str.cat():
                col_t = [c for c in df.columns if 'tmax' in c.lower()][0]
                df_base[f'tmax_{fuente}'] = df[col_t].values

            if 'obs_runoff' in df.columns.str.lower().str.cat() or 'q' in df.columns.str.lower().str.cat():
                col_q = [c for c in df.columns if 'runoff' in c.lower() or c.lower()=='q'][0]
                df_base['qobs'] = df[col_q].values

        # Separar forzamiento y caudal
        cols_forz = ['fecha'] + [c for c in df_base.columns if 'prcp' in c or 'tmax' in c or 'temp' in c]
        cols_caud = ['fecha', 'qobs'] if 'qobs' in df_base.columns else ['fecha']

        forzamiento = df_base[cols_forz].dropna()
        caudal = df_base[cols_caud].dropna()

        # Guardar en parquet
        print("\n4. Guardando en formato parquet...")
        forzamiento.to_parquet(DATOS / 'forzamiento.parquet', compression='snappy')
        caudal.to_parquet(DATOS / 'caudal.parquet', compression='snappy')

        # También CSV para compatibilidad
        forzamiento.to_csv(DATOS / 'forzamiento.csv', index=False)
        caudal.to_csv(DATOS / 'caudal.csv', index=False)

        print(f"\n✓ Datos guardados:")
        print(f"  - forzamiento.parquet: {len(forzamiento)} días, {forzamiento.memory_usage().sum()/1024:.1f} KB")
        print(f"  - caudal.parquet: {len(caudal)} días, {caudal.memory_usage().sum()/1024:.1f} KB")
        print(f"\nColumnas forzamiento: {list(forzamiento.columns)}")
        print(f"Columnas caudal: {list(caudal.columns)}")

        # Estadísticas
        print(f"\n5. Estadísticas:")
        print(f"Período: {forzamiento['fecha'].min()} a {forzamiento['fecha'].max()}")
        for col in [c for c in forzamiento.columns if 'prcp' in c]:
            print(f"{col}: media={forzamiento[col].mean():.2f} mm/d, max={forzamiento[col].max():.2f}")
        if 'qobs' in caudal.columns:
            print(f"qobs: media={caudal['qobs'].mean():.3f} mm/d, max={caudal['qobs'].max():.3f}")
    else:
        print("✗ No se encontraron datos para la cuenca seleccionada")
        print("\nINSTRUCCIONES MANUALES:")
        print("1. Descarga manual desde: https://ral.ucar.edu/solutions/products/camels")
        print(f"2. Busca archivos con ID {gauge_id}")
        print("3. Colócalos en datos/")
else:
    print("\n✗ No se pudo descargar. Descarga manual:")
    print("\n1. Ve a: https://ral.ucar.edu/solutions/products/camels")
    print("2. O mejor: https://zenodo.org/records/15529996")
    print("3. Descarga: basin_timeseries_v1p2_modelOutput_daymet.zip")
    print(f"4. Busca archivos de cuenca {gauge_id}")
    print(f"5. Ejecuta: python 00_procesar_manual.py")
