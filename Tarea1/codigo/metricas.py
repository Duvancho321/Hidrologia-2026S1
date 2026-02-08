"""Métricas de evaluación hidrológica

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Implementación de métricas NSE, KGE, RMSE, PBIAS.
"""
from numpy import sum, mean, sqrt, corrcoef

def nse(obs, sim):
    """Nash-Sutcliffe Efficiency"""
    return 1 - sum((obs - sim)**2) / sum((obs - obs.mean())**2)

def kge(obs, sim):
    """Kling-Gupta Efficiency"""
    r = corrcoef(obs, sim)[0,1]  # Correlación
    alpha = sim.std() / obs.std()    # Variabilidad relativa
    beta = sim.mean() / obs.mean()   # Sesgo relativo
    return 1 - sqrt((r-1)**2 + (alpha-1)**2 + (beta-1)**2), r, alpha, beta

def rmse(obs, sim):
    """Root Mean Square Error"""
    return sqrt(mean((obs - sim)**2))

def pbias(obs, sim):
    """Percent Bias"""
    return 100 * sum(sim - obs) / sum(obs)

def metricas_completas(obs, sim):
    """Calcular todas las métricas"""
    kge_val, r, alpha, beta = kge(obs, sim)
    return {
        'NSE': nse(obs, sim),
        'KGE': kge_val,
        'r': r,
        'alpha': alpha,
        'beta': beta,
        'RMSE': rmse(obs, sim),
        'PBIAS': pbias(obs, sim)
    }
