"""Comparación detallada de las 3 fuentes de precipitación

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Comparación de fuentes de precipitación Daymet, Maurer y NLDAS.
"""
from pandas import read_csv, DataFrame
from numpy import corrcoef
from matplotlib import pyplot as plt
from pathlib import Path
from modelo import DosTanques
from metricas import metricas_completas

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'

# Cargar datos
params = read_csv(DATOS / 'parametros_optimos.csv')['valor'].values
forz = read_csv(DATOS / 'forzamiento.csv', parse_dates=['fecha'])
caud = read_csv(DATOS / 'caudal.csv', parse_dates=['fecha'])
df = forz.merge(caud, on='fecha')

# Identificar fuentes disponibles
fuentes_p = [c.replace('prcp_', '') for c in df.columns if 'prcp_' in c]
mask_cal = (df['fecha'] >= '1990-01-01') & (df['fecha'] <= '2000-12-31')

print("="*70)
print("COMPARACIÓN DE FUENTES DE PRECIPITACIÓN")
print("="*70)
print(f"\nFuentes disponibles: {', '.join(fuentes_p)}")

# Comparar estadísticas
print(f"\n{'Fuente':<10} {'P media':>10} {'P std':>10} {'P max':>10} {'Correlación':>12}")
print("-"*54)

resultados = []
for fuente in fuentes_p:
    P = df[mask_cal][f'prcp_{fuente}'].values
    Q_obs = df[mask_cal]['qobs'].values

    # Calibrar con esta fuente
    modelo = DosTanques.from_array(params)
    Qsim, _, _ = modelo.run(P)
    metricas = metricas_completas(Q_obs, Qsim)

    # Correlación con primera fuente
    corr_p = corrcoef(P, df[mask_cal][f'prcp_{fuentes_p[0]}'].values)[0,1]

    print(f"{fuente.upper():<10} {P.mean():>10.3f} {P.std():>10.3f} "
          f"{P.max():>10.3f} {corr_p:>12.4f}")

    resultados.append({
        'Fuente': fuente.upper(),
        'P_mean': P.mean(),
        'P_std': P.std(),
        'P_max': P.max(),
        'NSE': metricas['NSE'],
        'KGE': metricas['KGE'],
        'RMSE': metricas['RMSE']
    })

# Guardar resultados
df_comp = DataFrame(resultados)
df_comp.to_csv(DATOS / 'comparacion_fuentes.csv', index=False)

print(f"\n{'Fuente':<10} {'NSE':>10} {'KGE':>10} {'RMSE':>10}")
print("-"*42)
for _, row in df_comp.iterrows():
    print(f"{row['Fuente']:<10} {row['NSE']:>10.4f} {row['KGE']:>10.4f} {row['RMSE']:>10.4f}")

# Visualización
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Series temporales de precipitación
ax = axes[0, 0]
for fuente in fuentes_p:
    ax.plot(df[mask_cal]['fecha'], df[mask_cal][f'prcp_{fuente}'],
            alpha=0.7, lw=0.5, label=fuente.upper())
ax.set_ylabel('Precipitación (mm/d)'), ax.set_title('Series Temporales')
ax.legend(), ax.grid(True, alpha=0.3)

# 2. Scatter plots entre fuentes
ax = axes[0, 1]
if len(fuentes_p) >= 2:
    ax.scatter(df[mask_cal][f'prcp_{fuentes_p[0]}'],
              df[mask_cal][f'prcp_{fuentes_p[1]}'], alpha=0.3, s=10)
    lim = [0, max(df[mask_cal][f'prcp_{fuentes_p[0]}'].max(),
                  df[mask_cal][f'prcp_{fuentes_p[1]}'].max())]
    ax.plot(lim, lim, 'r--', lw=1)
    ax.set_xlabel(f'{fuentes_p[0].upper()} (mm/d)')
    ax.set_ylabel(f'{fuentes_p[1].upper()} (mm/d)')
    corr = corrcoef(df[mask_cal][f'prcp_{fuentes_p[0]}'],
                       df[mask_cal][f'prcp_{fuentes_p[1]}'])[0,1]
    ax.set_title(f'Comparación {fuentes_p[0].upper()} vs {fuentes_p[1].upper()}\nr = {corr:.4f}')
    ax.grid(True, alpha=0.3)

# 3. NSE por fuente
ax = axes[1, 0]
ax.bar(df_comp['Fuente'], df_comp['NSE'], alpha=0.8, edgecolor='black')
ax.set_ylabel('NSE'), ax.set_title('Nash-Sutcliffe Efficiency por Fuente')
ax.axhline(0.5, color='g', linestyle='--', lw=1, label='Satisfactorio')
ax.axhline(0, color='r', linestyle='--', lw=1)
ax.legend(), ax.grid(True, alpha=0.3, axis='y')

# 4. KGE por fuente
ax = axes[1, 1]
ax.bar(df_comp['Fuente'], df_comp['KGE'], alpha=0.8, edgecolor='black', color='orange')
ax.set_ylabel('KGE'), ax.set_title('Kling-Gupta Efficiency por Fuente')
ax.axhline(0.5, color='g', linestyle='--', lw=1, label='Satisfactorio')
ax.axhline(0, color='r', linestyle='--', lw=1)
ax.legend(), ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(FIGS / 'comparacion_fuentes_detallada.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Gráfica guardada: {FIGS / 'comparacion_fuentes_detallada.png'}")
print(f"✓ Resultados guardados: {DATOS / 'comparacion_fuentes.csv'}")
