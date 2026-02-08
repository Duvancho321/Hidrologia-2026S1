"""Tarea 1 - Parte 1: Exploración y Selección de Cuencas CAMELS

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Implementación de exploración y selección automática de cuencas.
"""
from pandas import read_csv, DataFrame
from numpy import linspace
from matplotlib import pyplot as plt
from pathlib import Path

DATOS = Path(__file__).parent.parent / 'datos'
FIGS = Path(__file__).parent.parent / 'figuras'
FIGS.mkdir(exist_ok=True)

# Cargar y filtrar en una línea
df = read_csv(DATOS / 'cuencas_validas.csv')
df_filt = df[(df['area_gages2'] < 500) & (df['frac_snow'] <= 0.10)].copy()

# Seleccionar mejor cuenca: sin nieve, área 20-300 km², score alto
candidatos = df_filt[df_filt['frac_snow'] == 0.0] if (df_filt['frac_snow'] == 0.0).any() else df_filt.nsmallest(20, 'frac_snow')
candidatos = candidatos[(candidatos['area_gages2'] > 20) & (candidatos['area_gages2'] < 300)].copy()
candidatos['score'] = ((candidatos['p_mean'] > 1.0).astype(int) * 10 +
    (candidatos['q_mean'] > 0.1).astype(int) * 5 + (300 - candidatos['area_gages2']) / 300 * 3)
mejor = candidatos.sort_values('score', ascending=False).iloc[0]

# Guardar selección
DataFrame([mejor]).to_csv(DATOS / 'cuenca_seleccionada.csv', index=False)

# Graficar
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.suptitle('Distribución de Cuencas CAMELS', fontsize=16, fontweight='bold')

# Área vs nieve
axs[0,0].scatter(df['area_gages2'], df['frac_snow'], alpha=0.3, s=20, label='Todas')
axs[0,0].scatter(df_filt['area_gages2'], df_filt['frac_snow'], alpha=0.7, s=30, c='red', label='Filtradas')
axs[0,0].axhline(0.10, color='orange', linestyle='--', label='Max nieve (0.10)')
axs[0,0].axvline(500, color='green', linestyle='--', label='Max área (500 km²)')
axs[0,0].set_xlabel('Área (km²)'), axs[0,0].set_ylabel('Fracción de nieve')
axs[0,0].set_xscale('log'), axs[0,0].legend(), axs[0,0].grid(True, alpha=0.3)

# Histograma área
axs[0,1].hist(df['area_gages2'], bins=50, alpha=0.5, label='Todas', edgecolor='black')
axs[0,1].hist(df_filt['area_gages2'], bins=30, alpha=0.7, label='Filtradas', edgecolor='black', color='red')
axs[0,1].axvline(500, color='green', linestyle='--', linewidth=2)
axs[0,1].set_xlabel('Área (km²)'), axs[0,1].set_ylabel('Frecuencia')
axs[0,1].legend(), axs[0,1].grid(True, alpha=0.3)

# Histograma nieve
axs[1,0].hist(df['frac_snow'], bins=linspace(0, df['frac_snow'].max(), 50), alpha=0.5, label='Todas', edgecolor='black')
axs[1,0].hist(df_filt['frac_snow'], bins=30, alpha=0.7, label='Filtradas', edgecolor='black', color='red')
axs[1,0].axvline(0.10, color='orange', linestyle='--', linewidth=2)
axs[1,0].set_xlabel('Fracción de nieve'), axs[1,0].set_ylabel('Frecuencia')
axs[1,0].legend(), axs[1,0].grid(True, alpha=0.3)

# Precipitación vs caudal
sc = axs[1,1].scatter(df_filt['p_mean'], df_filt['q_mean'], c=df_filt['area_gages2'], s=50, alpha=0.7, cmap='viridis')
axs[1,1].set_xlabel('Precipitación media (mm/día)'), axs[1,1].set_ylabel('Caudal medio (mm/día)')
axs[1,1].grid(True, alpha=0.3)
plt.colorbar(sc, ax=axs[1,1]).set_label('Área (km²)')

plt.tight_layout()
plt.savefig(FIGS / 'exploracion_cuencas.png', dpi=300, bbox_inches='tight')

# Resultados
print(f"Total cuencas: {len(df)} | Filtradas: {len(df_filt)} | Sin nieve: {(df_filt['frac_snow']==0).sum()}")
print(f"\nCUENCA SELECCIONADA: {mejor['gauge_id']}")
print(f"Área: {mejor['area_gages2']:.2f} km² | Nieve: {mejor['frac_snow']*100:.2f}%")
print(f"P: {mejor['p_mean']:.2f} mm/d | Q: {mejor['q_mean']:.3f} mm/d | Score: {mejor['score']:.2f}")
print(f"\nTop 5 candidatos:\n{candidatos.head()[['gauge_id','area_gages2','frac_snow','p_mean','q_mean','score']]}")
