"""Análisis avanzado: KGE, scatter plots, curvas de duración, sensibilidad

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Análisis avanzado con KGE, sensibilidad y 9 visualizaciones.
"""
from pandas import read_csv, DataFrame
from numpy import (arange, sum, sort, sqrt, corrcoef, array)
from matplotlib import pyplot as plt
from scipy import stats
from pathlib import Path
from modelo import DosTanques
from metricas import metricas_completas

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'

# Cargar datos y parámetros
params = read_csv(DATOS / 'parametros_optimos.csv')['valor'].values
forz = read_csv(DATOS / 'forzamiento.csv', parse_dates=['fecha'])
caud = read_csv(DATOS / 'caudal.csv', parse_dates=['fecha'])
df = forz.merge(caud, on='fecha')

# Períodos
mask_cal = (df['fecha'] >= '1990-01-01') & (df['fecha'] <= '2000-12-31')
mask_val = (df['fecha'] >= '2000-01-01') & (df['fecha'] <= '2010-12-31')

# Simular
modelo = DosTanques.from_array(params)
P_cal, Q_obs_cal = df[mask_cal]['prcp_daymet'].values, df[mask_cal]['qobs'].values
P_val, Q_obs_val = df[mask_val]['prcp_daymet'].values, df[mask_val]['qobs'].values
Qsim_cal, S1_cal, S2_cal = modelo.run(P_cal)
Qsim_val, S1_val, S2_val = modelo.run(P_val)

# Métricas completas
met_cal = metricas_completas(Q_obs_cal, Qsim_cal)
met_val = metricas_completas(Q_obs_val, Qsim_val)

print("="*60)
print("MÉTRICAS DE DESEMPEÑO")
print("="*60)
print(f"\n{'Métrica':<10} {'Calibración':>12} {'Validación':>12}")
print("-"*36)
for k in ['NSE', 'KGE', 'r', 'alpha', 'beta', 'RMSE', 'PBIAS']:
    print(f"{k:<10} {met_cal[k]:>12.4f} {met_val[k]:>12.4f}")

# Guardar métricas
DataFrame({'Calibracion': met_cal, 'Validacion': met_val}).to_csv(
    DATOS / 'metricas_completas.csv')

# === VISUALIZACIONES AVANZADAS ===

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Scatter plot Obs vs Sim (Calibración)
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(Q_obs_cal, Qsim_cal, alpha=0.3, s=10, c='blue')
lim = [0, max(Q_obs_cal.max(), Qsim_cal.max())]
ax1.plot(lim, lim, 'k--', lw=1, label='1:1')
ax1.set_xlabel('Q observado (mm/d)'), ax1.set_ylabel('Q simulado (mm/d)')
ax1.set_title(f'Calibración\nNSE={met_cal["NSE"]:.3f}, KGE={met_cal["KGE"]:.3f}')
ax1.legend(), ax1.grid(True, alpha=0.3)

# 2. Scatter plot Obs vs Sim (Validación)
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(Q_obs_val, Qsim_val, alpha=0.3, s=10, c='red')
lim = [0, max(Q_obs_val.max(), Qsim_val.max())]
ax2.plot(lim, lim, 'k--', lw=1, label='1:1')
ax2.set_xlabel('Q observado (mm/d)'), ax2.set_ylabel('Q simulado (mm/d)')
ax2.set_title(f'Validación\nNSE={met_val["NSE"]:.3f}, KGE={met_val["KGE"]:.3f}')
ax2.legend(), ax2.grid(True, alpha=0.3)

# 3. Curva de duración (Calibración)
ax3 = fig.add_subplot(gs[0, 2])
q_obs_sort = sort(Q_obs_cal)[::-1]
q_sim_sort = sort(Qsim_cal)[::-1]
exc = 100 * arange(1, len(q_obs_sort)+1) / len(q_obs_sort)
ax3.semilogy(exc, q_obs_sort, 'k-', lw=1.5, label='Observado')
ax3.semilogy(exc, q_sim_sort, 'r-', lw=1.5, label='Simulado')
ax3.set_xlabel('Probabilidad de excedencia (%)'), ax3.set_ylabel('Caudal (mm/d)')
ax3.set_title('Curva de Duración - Calibración')
ax3.legend(), ax3.grid(True, alpha=0.3, which='both')

# 4. Residuos vs Q observado
ax4 = fig.add_subplot(gs[1, 0])
residuos = Q_obs_cal - Qsim_cal
ax4.scatter(Q_obs_cal, residuos, alpha=0.3, s=10, c='blue')
ax4.axhline(0, color='k', linestyle='--', lw=1)
ax4.set_xlabel('Q observado (mm/d)'), ax4.set_ylabel('Residuos (mm/d)')
ax4.set_title('Residuos vs Q observado')
ax4.grid(True, alpha=0.3)

# 5. Histograma de residuos
ax5 = fig.add_subplot(gs[1, 1])
ax5.hist(residuos, bins=50, edgecolor='black', alpha=0.7)
ax5.axvline(0, color='r', linestyle='--', lw=2)
ax5.set_xlabel('Residuos (mm/d)'), ax5.set_ylabel('Frecuencia')
ax5.set_title(f'Distribución de Residuos\nMedia={residuos.mean():.4f}')
ax5.grid(True, alpha=0.3)

# 6. Almacenamiento en tanques
ax6 = fig.add_subplot(gs[1, 2])
fechas_cal = df[mask_cal]['fecha'].values
ax6.plot(fechas_cal, S1_cal, 'b-', alpha=0.7, lw=0.8, label='S1 (Suelo)')
ax6.plot(fechas_cal, S2_cal, 'r-', alpha=0.7, lw=0.8, label='S2 (Subterráneo)')
ax6.axhline(params[3], color='b', linestyle='--', lw=1, alpha=0.5, label=f'D1={params[3]:.0f}')
ax6.axhline(params[6], color='r', linestyle='--', lw=1, alpha=0.5, label=f'D2={params[6]:.0f}')
ax6.set_xlabel('Fecha'), ax6.set_ylabel('Almacenamiento (mm)')
ax6.set_title('Evolución de Almacenamiento')
ax6.legend(), ax6.grid(True, alpha=0.3)

# 7. Q-Q plot
ax7 = fig.add_subplot(gs[2, 0])
stats.probplot(residuos, dist="norm", plot=ax7)
ax7.set_title('Q-Q Plot de Residuos')
ax7.grid(True, alpha=0.3)

# 8. Autocorrelación de residuos
ax8 = fig.add_subplot(gs[2, 1])
lags = arange(0, 100)
autocorr = [corrcoef(residuos[:-lag if lag > 0 else None],
                        residuos[lag:])[0,1] if lag > 0 else 1
            for lag in lags]
ax8.bar(lags, autocorr, width=1, edgecolor='black')
ax8.axhline(0, color='k', lw=1)
ax8.axhline(1.96/sqrt(len(residuos)), color='r', linestyle='--', lw=1)
ax8.axhline(-1.96/sqrt(len(residuos)), color='r', linestyle='--', lw=1)
ax8.set_xlabel('Lag (días)'), ax8.set_ylabel('Autocorrelación')
ax8.set_title('Autocorrelación de Residuos')
ax8.grid(True, alpha=0.3)

# 9. Componentes KGE
ax9 = fig.add_subplot(gs[2, 2])
componentes = ['r\n(correlación)', 'α\n(variabilidad)', 'β\n(sesgo)']
valores_cal = [met_cal['r'], met_cal['alpha'], met_cal['beta']]
valores_val = [met_val['r'], met_val['alpha'], met_val['beta']]
x = arange(len(componentes))
width = 0.35
ax9.bar(x - width/2, valores_cal, width, label='Calibración', alpha=0.8)
ax9.bar(x + width/2, valores_val, width, label='Validación', alpha=0.8)
ax9.axhline(1, color='r', linestyle='--', lw=1, label='Ideal')
ax9.set_ylabel('Valor'), ax9.set_title('Componentes KGE')
ax9.set_xticks(x), ax9.set_xticklabels(componentes)
ax9.legend(), ax9.grid(True, alpha=0.3, axis='y')

plt.suptitle('Análisis Avanzado del Modelo', fontsize=16, fontweight='bold', y=0.995)
plt.savefig(FIGS / 'analisis_avanzado.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Gráfica guardada: {FIGS / 'analisis_avanzado.png'}")

# === ANÁLISIS DE SENSIBILIDAD ===
print("\n" + "="*60)
print("ANÁLISIS DE SENSIBILIDAD (variación ±20%)")
print("="*60)

sens_results = []
param_names = ['ETc', 'beta', 'alpha1', 'D1', 'k1', 'alpha2', 'D2', 'k2']

for i, pname in enumerate(param_names):
    params_test = params.copy()

    # +20%
    params_test[i] = params[i] * 1.2
    Qsim_plus, _, _ = DosTanques.from_array(params_test).run(P_cal)
    nse_plus = 1 - sum((Q_obs_cal - Qsim_plus)**2) / sum((Q_obs_cal - Q_obs_cal.mean())**2)

    # -20%
    params_test[i] = params[i] * 0.8
    Qsim_minus, _, _ = DosTanques.from_array(params_test).run(P_cal)
    nse_minus = 1 - sum((Q_obs_cal - Qsim_minus)**2) / sum((Q_obs_cal - Q_obs_cal.mean())**2)

    # Sensibilidad: cambio en NSE por cambio en parámetro
    sensibilidad = (nse_plus - nse_minus) / (0.4 * params[i]) if params[i] > 0 else 0

    sens_results.append({
        'Parametro': pname,
        'Valor_base': params[i],
        'NSE_base': met_cal['NSE'],
        'NSE_+20%': nse_plus,
        'NSE_-20%': nse_minus,
        'Sensibilidad': abs(sensibilidad)
    })

df_sens = DataFrame(sens_results).sort_values('Sensibilidad', ascending=False)
print(df_sens[['Parametro', 'NSE_+20%', 'NSE_-20%', 'Sensibilidad']].to_string(index=False))
df_sens.to_csv(DATOS / 'sensibilidad.csv', index=False)

print(f"\n✓ Análisis completado")
print(f"✓ Métricas guardadas: {DATOS / 'metricas_completas.csv'}")
print(f"✓ Sensibilidad guardada: {DATOS / 'sensibilidad.csv'}")
