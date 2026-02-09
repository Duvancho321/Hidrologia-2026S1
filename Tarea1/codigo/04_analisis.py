"""Tarea 1 - Parte 5: Análisis y Comparación

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Análisis de parámetros calibrados y comparación de fuentes.
"""
from pandas import read_csv, DataFrame
from numpy import sum
from matplotlib import pyplot as plt
from pathlib import Path
from src.modelos import DosTanques
from src.metricas import nse

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'

# Cargar resultados
params = read_csv(DATOS / 'parametros_optimos.csv')
forz = read_csv(DATOS / 'forzamiento.csv', parse_dates=['fecha'])
caud = read_csv(DATOS / 'caudal.csv', parse_dates=['fecha'])
cuenca = read_csv(DATOS / 'cuenca_seleccionada.csv').iloc[0]

# Interpretación física de parámetros
print("="*80)
print("INTERPRETACIÓN FÍSICA DE PARÁMETROS CALIBRADOS")
print("="*80)
interpretacion = {
    'ETc': f"{params.iloc[0]['valor']:.3f} mm/d - Evapotranspiración base {'muy baja' if params.iloc[0]['valor']<1 else 'normal'}",
    'beta': f"{params.iloc[1]['valor']:.3f} - {'Alta' if params.iloc[1]['valor']>0.5 else 'Baja'} fracción de P que se evapora",
    'alpha1': f"{params.iloc[2]['valor']:.3f} - {'Alta' if params.iloc[2]['valor']>0.3 else 'Baja'} escorrentía directa",
    'D1': f"{params.iloc[3]['valor']:.1f} mm - Capacidad del suelo {'pequeña' if params.iloc[3]['valor']<150 else 'grande'}",
    'k1': f"{params.iloc[4]['valor']:.4f} - Drenaje del suelo {'rápido' if params.iloc[4]['valor']>0.1 else 'lento'}",
    'alpha2': f"{params.iloc[5]['valor']:.3f} - {'Alto' if params.iloc[5]['valor']>0.5 else 'Bajo'} flujo rápido subterráneo",
    'D2': f"{params.iloc[6]['valor']:.1f} mm - Capacidad del acuífero {'pequeña' if params.iloc[6]['valor']<500 else 'grande'}",
    'k2': f"{params.iloc[7]['valor']:.4f} - Descarga del acuífero {'rápida' if params.iloc[7]['valor']>0.01 else 'lenta'}"
}
for param, interp in interpretacion.items():
    print(f"{param:8s}: {interp}")

# Comparar fuentes de precipitación (si hay múltiples)
df = forz.merge(caud, on='fecha')
mask_cal = (df['fecha'] >= '1990-01-01') & (df['fecha'] <= '2000-12-31')

fuentes_p = [col for col in df.columns if 'prcp' in col]
if len(fuentes_p) > 1:
    print(f"\n{'='*80}\nCOMPARACIÓN DE FUENTES DE PRECIPITACIÓN\n{'='*80}")

    modelo = DosTanques.from_array(params['valor'].values)
    resultados_fuentes = []

    for fuente in fuentes_p:
        P = df[mask_cal][fuente].values
        Q_obs = df[mask_cal]['qobs'].values
        Qsim, _, _ = modelo.run(P)
        nse_val = nse(Q_obs, Qsim)
        resultados_fuentes.append({'Fuente': fuente.replace('prcp_', '').upper(),
                                   'P_mean': P.mean(), 'NSE': nse_val})

    res_df = DataFrame(resultados_fuentes)
    print(res_df.to_string(index=False))

    # Graficar comparación
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(res_df['Fuente'], res_df['NSE'], color=['blue', 'green', 'orange'])
    ax.set_ylabel('NSE'), ax.set_xlabel('Fuente de Precipitación')
    ax.set_title('Comparación de Fuentes de Precipitación', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(FIGS / 'comparacion_precip.png', dpi=300, bbox_inches='tight')
    print(f"\nGráfica guardada: {FIGS / 'comparacion_precip.png'}")

# Análisis de balance hídrico
print(f"\n{'='*80}\nBALANCE HÍDRICO\n{'='*80}")
P_total = df[mask_cal]['prcp_daymet'].sum()
Q_total = df[mask_cal]['qobs'].sum()
ET_estimada = P_total - Q_total
coef_escorrentia = Q_total / P_total if P_total > 0 else 0

print(f"Precipitación total: {P_total:.1f} mm")
print(f"Caudal total: {Q_total:.1f} mm")
print(f"ET estimada (P-Q): {ET_estimada:.1f} mm")
print(f"Coeficiente de escorrentía: {coef_escorrentia:.3f}")

# Limitaciones del modelo
print(f"\n{'='*80}\nLIMITACIONES DEL MODELO\n{'='*80}")
limitaciones = [
    "1. Estructura simple (solo 2 tanques) - no representa todos los procesos",
    "2. No incluye intercepción ni almacenamiento de nieve",
    "3. Parámetros constantes en el tiempo (no variabilidad estacional)",
    "4. No considera heterogeneidad espacial dentro de la cuenca",
    "5. ET simplificada (no considera radiación, viento, humedad)",
    "6. Datos sintéticos (no representan dinámica real de la cuenca)"
]
for lim in limitaciones:
    print(lim)

print(f"\n{'='*80}\nMEJORAS PROPUESTAS\n{'='*80}")
mejoras = [
    "1. Agregar módulo de nieve si hay fracción de nieve significativa",
    "2. Incluir intercepción en dosel vegetal",
    "3. Usar ET potencial (Penman-Monteith) en lugar de ET base constante",
    "4. Considerar variabilidad estacional de parámetros",
    "5. Calibración multi-objetivo (NSE + KGE + volumen)",
    "6. Validación con datos independientes de diferentes períodos climáticos"
]
for mej in mejoras:
    print(mej)
