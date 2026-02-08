"""Tarea 1 - Parte 2: Preparar datos de cuenca seleccionada

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Preparación de datos meteorológicos y generación de datos sintéticos.
"""
from pandas import read_csv, DataFrame, date_range, Timestamp
from numpy import (arange, maximum, random, sin, pi, convolve, exp, linspace)
from matplotlib import pyplot as plt
from pathlib import Path

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'
CAMELS_DIR = Path.home() / 'camels_data'  # Ajustar según ubicación

# Cargar cuenca seleccionada
cuenca = read_csv(DATOS / 'cuenca_seleccionada.csv').iloc[0]
gauge_id = str(int(cuenca['gauge_id']))

# Función para cargar datos CAMELS (MODIFICAR según estructura real de CAMELS)
def cargar_camels(gauge_id, camels_dir=CAMELS_DIR):
    """Cargar forzamiento meteorológico y caudal de CAMELS"""
    # Estructura típica CAMELS:
    # basin_timeseries_v1p2_modelOutput_daymet/XX/XXXXXXXX_model_output_daymet.txt
    basin_dir = camels_dir / 'basin_timeseries_v1p2_modelOutput_daymet' / gauge_id[:2]

    # Intentar cargar cada fuente de precipitación
    fuentes = ['daymet', 'maurer', 'nldas']
    datos = {}

    for fuente in fuentes:
        try:
            # Ajustar path según estructura real
            file_pattern = f"{gauge_id}*{fuente}*.txt"
            archivo = list(basin_dir.glob(file_pattern))[0] if basin_dir.exists() else None

            if archivo and archivo.exists():
                df = read_csv(archivo, sep=r'\s+', comment='#')
                df['date'] = pd.to_datetime(df[['Year','Mnth','Day']] if 'Year' in df.columns
                                           else df.iloc[:,:3], errors='coerce')
                datos[fuente] = df
        except Exception as e:
            continue

    return datos if datos else None

# Intentar cargar datos reales de CAMELS
datos_camels = cargar_camels(gauge_id)

if datos_camels is None:
    # Si no hay datos CAMELS, crear datos sintéticos para probar el modelo
    print(f"No se encontraron datos CAMELS para {gauge_id}, generando datos sintéticos...")

    # Generar serie temporal 1980-2014
    fechas = date_range('1980-01-01', '2014-12-31', freq='D')
    n = len(fechas)

    # Precipitación sintética: proceso estocástico con estacionalidad
    random.seed(42)
    P_base = cuenca['p_mean']
    estacionalidad = 1 + 0.3 * sin(2 * pi * arange(n) / 365.25)
    P = maximum(0, P_base * estacionalidad * random.gamma(2, 0.5, n))

    # Caudal sintético: respuesta simplificada a precipitación
    Q = convolve(P, exp(-arange(30)/3)/10, mode='same') * (cuenca['q_mean']/P_base)
    Q += random.normal(0, 0.05, n)
    Q = maximum(0, Q)

    # DataFrame
    forzamiento = DataFrame({
        'fecha': fechas,
        'prcp_daymet': P,
        'prcp_maurer': P * random.uniform(0.9, 1.1, n),
        'prcp_nldas': P * random.uniform(0.9, 1.1, n),
        'temp': 15 + 10 * sin(2 * pi * arange(n) / 365.25) + random.normal(0, 2, n)
    })

    caudal = DataFrame({
        'fecha': fechas,
        'qobs': Q
    })

    print(f"Datos sintéticos generados: {len(forzamiento)} días")
else:
    # Procesar datos reales de CAMELS
    print(f"Datos CAMELS cargados para {gauge_id}")
    # Aquí iría el procesamiento real según datos reales
    forzamiento = None  # Completar según datos reales
    caudal = None

# Guardar datos procesados
forzamiento.to_csv(DATOS / 'forzamiento.csv', index=False)
caudal.to_csv(DATOS / 'caudal.csv', index=False)

# Estadísticas básicas por período
periodos = {
    'Completo': (forzamiento['fecha'].min(), forzamiento['fecha'].max()),
    'Calibración': ('1990-01-01', '2000-12-31'),
    'Validación': ('2000-01-01', '2010-12-31')
}

stats = DataFrame([{
    'Período': nombre,
    'P_mean': forzamiento[(forzamiento['fecha'] >= inicio) & (forzamiento['fecha'] <= fin)]['prcp_daymet'].mean(),
    'P_std': forzamiento[(forzamiento['fecha'] >= inicio) & (forzamiento['fecha'] <= fin)]['prcp_daymet'].std(),
    'P_max': forzamiento[(forzamiento['fecha'] >= inicio) & (forzamiento['fecha'] <= fin)]['prcp_daymet'].max(),
    'Q_mean': caudal[(caudal['fecha'] >= inicio) & (caudal['fecha'] <= fin)]['qobs'].mean(),
    'Q_std': caudal[(caudal['fecha'] >= inicio) & (caudal['fecha'] <= fin)]['qobs'].std(),
    'Q_max': caudal[(caudal['fecha'] >= inicio) & (caudal['fecha'] <= fin)]['qobs'].max()
} for nombre, (inicio, fin) in periodos.items()])

print(f"\n{stats.to_string(index=False)}")

# Graficar series temporales
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Precipitación
ax1.plot(forzamiento['fecha'], forzamiento['prcp_daymet'], 'b-', alpha=0.6, linewidth=0.5, label='Daymet')
ax1.plot(forzamiento['fecha'], forzamiento['prcp_maurer'], 'g-', alpha=0.4, linewidth=0.5, label='Maurer')
ax1.plot(forzamiento['fecha'], forzamiento['prcp_nldas'], 'orange', alpha=0.4, linewidth=0.5, label='NLDAS')
ax1.set_ylabel('Precipitación (mm/día)'), ax1.legend(loc='upper right'), ax1.grid(True, alpha=0.3)
ax1.set_title(f'Cuenca {gauge_id} - Series Temporales', fontweight='bold')

# Caudal
ax2.plot(caudal['fecha'], caudal['qobs'], 'k-', alpha=0.7, linewidth=0.7)
ax2.set_ylabel('Caudal (mm/día)'), ax2.set_xlabel('Fecha'), ax2.grid(True, alpha=0.3)

# Marcar períodos
for ax in (ax1, ax2):
    ax.axvspan(Timestamp('1990-01-01'), Timestamp('2000-12-31'), alpha=0.1, color='green', label='Calibración')
    ax.axvspan(Timestamp('2000-01-01'), Timestamp('2010-12-31'), alpha=0.1, color='orange', label='Validación')

plt.tight_layout()
plt.savefig(FIGS / 'series_tiempo.png', dpi=300, bbox_inches='tight')
print(f"\nGráfica guardada: {FIGS / 'series_tiempo.png'}")
