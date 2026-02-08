"""Tarea 1 - Parte 3-4: Implementación y Calibración del Modelo

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Calibración del modelo con Differential Evolution.
"""
from pandas import read_csv, DataFrame
from numpy import array, sum, zeros, ndarray
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution
from pathlib import Path
from modelo import DosTanques

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'

# Cargar datos
forz = read_csv(DATOS / 'forzamiento.csv', parse_dates=['fecha'])
caud = read_csv(DATOS / 'caudal.csv', parse_dates=['fecha'])
df = forz.merge(caud, on='fecha')

# Dividir períodos (excluir primeros 365 días de calentamiento)
mask_cal = (df['fecha'] >= '1990-01-01') & (df['fecha'] <= '2000-12-31')
mask_val = (df['fecha'] >= '2000-01-01') & (df['fecha'] <= '2010-12-31')
mask_warm = (df['fecha'] >= '1989-01-01') & (df['fecha'] < '1990-01-01')

# Datos de calibración/validación
P_cal, Q_obs_cal = df[mask_cal]['prcp_daymet'].values, df[mask_cal]['qobs'].values
P_val, Q_obs_val = df[mask_val]['prcp_daymet'].values, df[mask_val]['qobs'].values
P_warm = df[mask_warm]['prcp_daymet'].values if mask_warm.sum() >= 365 else zeros(365)

# Función objetivo NSE (minimizar -NSE = maximizar NSE)
def nse(Qobs, Qsim):
    return 1 - sum((Qobs - Qsim)**2) / sum((Qobs - Qobs.mean())**2)

# Función objetivo para optimización
def objetivo(params):
    modelo = DosTanques.from_array(params)
    # Warm-up con primeros 365 días
    _, S1_warm, S2_warm = modelo.run(P_warm) if len(P_warm) == 365 else (None, 0, 0)
    S1_0, S2_0 = (S1_warm[-1], S2_warm[-1]) if isinstance(S1_warm, ndarray) else (0, 0)
    # Calibración
    Qsim, _, _ = modelo.run(P_cal, S1_0, S2_0)
    return -nse(Q_obs_cal, Qsim)  # Minimizar -NSE

# Límites de parámetros: [ETc, beta, alpha1, D1, k1, alpha2, D2, k2]
bounds = [(0, 10), (0, 1), (0, 1), (10, 500), (0.001, 0.99),
          (0, 1), (10, 1000), (0.001, 0.99)]

# Parámetros por defecto para prueba inicial
params_def = array([2.0, 0.3, 0.1, 200.0, 0.1, 0.3, 500.0, 0.01])
modelo_def = DosTanques.from_array(params_def)
Qsim_def, _, _ = modelo_def.run(P_cal)
nse_def = nse(Q_obs_cal, Qsim_def)
print(f"NSE con parámetros por defecto: {nse_def:.4f}")

# Calibración con Differential Evolution
print("\nIniciando calibración...")
resultado = differential_evolution(objetivo, bounds, maxiter=100, seed=42,
                                   workers=1, updating='deferred', disp=True)

params_opt = resultado.x
nse_cal = -resultado.fun
print(f"\nCalibración completada!")
print(f"NSE calibración: {nse_cal:.4f}")

# Validación
modelo_opt = DosTanques.from_array(params_opt)
Qsim_val, _, _ = modelo_opt.run(P_val)
nse_val = nse(Q_obs_val, Qsim_val)
print(f"NSE validación: {nse_val:.4f}")

# Guardar parámetros
param_names = ['ETc', 'beta', 'alpha1', 'D1', 'k1', 'alpha2', 'D2', 'k2']
params_df = DataFrame({'parametro': param_names, 'valor': params_opt})
params_df.to_csv(DATOS / 'parametros_optimos.csv', index=False)
print(f"\nParámetros óptimos:\n{params_df.to_string(index=False)}")

# Simular serie completa de calibración y validación
Qsim_cal_final, S1_cal, S2_cal = modelo_opt.run(P_cal)
Qsim_val_final, S1_val, S2_val = modelo_opt.run(P_val)

# Graficar resultados calibración
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

fechas_cal = df[mask_cal]['fecha'].values
ax1.plot(fechas_cal, Q_obs_cal, 'k-', alpha=0.7, linewidth=0.8, label='Observado')
ax1.plot(fechas_cal, Qsim_cal_final, 'r-', alpha=0.7, linewidth=0.8, label='Simulado')
ax1.set_ylabel('Caudal (mm/día)'), ax1.legend(), ax1.grid(True, alpha=0.3)
ax1.set_title(f'Calibración (1990-2000) - NSE: {nse_cal:.4f}', fontweight='bold')

ax2.plot(fechas_cal, Q_obs_cal - Qsim_cal_final, 'b-', alpha=0.5, linewidth=0.6)
ax2.axhline(0, color='k', linestyle='--', linewidth=1)
ax2.set_ylabel('Residuos (mm/día)'), ax2.set_xlabel('Fecha'), ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGS / 'calibracion.png', dpi=300, bbox_inches='tight')

# Graficar resultados validación
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

fechas_val = df[mask_val]['fecha'].values
ax1.plot(fechas_val, Q_obs_val, 'k-', alpha=0.7, linewidth=0.8, label='Observado')
ax1.plot(fechas_val, Qsim_val_final, 'r-', alpha=0.7, linewidth=0.8, label='Simulado')
ax1.set_ylabel('Caudal (mm/día)'), ax1.legend(), ax1.grid(True, alpha=0.3)
ax1.set_title(f'Validación (2000-2010) - NSE: {nse_val:.4f}', fontweight='bold')

ax2.plot(fechas_val, Q_obs_val - Qsim_val_final, 'b-', alpha=0.5, linewidth=0.6)
ax2.axhline(0, color='k', linestyle='--', linewidth=1)
ax2.set_ylabel('Residuos (mm/día)'), ax2.set_xlabel('Fecha'), ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(FIGS / 'validacion.png', dpi=300, bbox_inches='tight')

print(f"\nGráficas guardadas en {FIGS}")
