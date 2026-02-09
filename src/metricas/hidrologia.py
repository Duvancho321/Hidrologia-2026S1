"""Métricas de evaluación hidrológica

Implementación de métricas estándar para evaluar el desempeño de
modelos hidrológicos, incluyendo NSE, KGE, RMSE y PBIAS.

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintainer__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Implementación de métricas NSE, KGE, RMSE, PBIAS.
   - [2026-02-09]: Migración a módulo central src/metricas/
"""
from numpy import sum, mean, sqrt, corrcoef


def nse(obs, sim):
    """Calcular Nash-Sutcliffe Efficiency.

    El NSE varía de -∞ a 1, donde 1 indica ajuste perfecto,
    0 indica que el modelo es tan bueno como la media observada,
    y valores negativos indican que la media es mejor predictor.

    Parámetros
    ----------
    obs : ndarray
        Valores observados
    sim : ndarray
        Valores simulados

    Retorna
    -------
    float
        Coeficiente NSE

    Referencias
    -----------
    Nash, J. E., & Sutcliffe, J. V. (1970). River flow forecasting
    through conceptual models part I. Journal of Hydrology, 10(3), 282-290.
    """
    return 1 - sum((obs - sim)**2) / sum((obs - obs.mean())**2)


def kge(obs, sim):
    """Calcular Kling-Gupta Efficiency.

    El KGE descompone el desempeño en tres componentes: correlación,
    sesgo de variabilidad y sesgo de media. Varía de -∞ a 1, donde
    1 indica ajuste perfecto.

    Parámetros
    ----------
    obs : ndarray
        Valores observados
    sim : ndarray
        Valores simulados

    Retorna
    -------
    kge_val : float
        Coeficiente KGE
    r : float
        Correlación de Pearson
    alpha : float
        Ratio de desviaciones estándar (std_sim/std_obs)
    beta : float
        Ratio de medias (mean_sim/mean_obs)

    Referencias
    -----------
    Gupta, H. V., et al. (2009). Decomposition of the mean squared error
    and NSE performance criteria. Journal of Hydrology, 377(1-2), 80-91.
    """
    r = corrcoef(obs, sim)[0, 1]      # Correlación
    alpha = sim.std() / obs.std()      # Variabilidad relativa
    beta = sim.mean() / obs.mean()     # Sesgo relativo
    kge_val = 1 - sqrt((r-1)**2 + (alpha-1)**2 + (beta-1)**2)
    return kge_val, r, alpha, beta


def rmse(obs, sim):
    """Calcular Root Mean Square Error.

    Mide la magnitud promedio del error. Valores más bajos indican
    mejor ajuste, con 0 siendo perfecto. Tiene las mismas unidades
    que las variables observadas/simuladas.

    Parámetros
    ----------
    obs : ndarray
        Valores observados
    sim : ndarray
        Valores simulados

    Retorna
    -------
    float
        RMSE en las mismas unidades que obs/sim
    """
    return sqrt(mean((obs - sim)**2))


def pbias(obs, sim):
    """Calcular Percent Bias.

    Mide la tendencia promedio de los valores simulados a ser mayores
    o menores que los observados. Valores óptimos están cerca de 0,
    valores positivos indican sesgo de subestimación, y valores
    negativos indican sesgo de sobreestimación.

    Parámetros
    ----------
    obs : ndarray
        Valores observados
    sim : ndarray
        Valores simulados

    Retorna
    -------
    float
        PBIAS en porcentaje
    """
    return 100 * sum(sim - obs) / sum(obs)


def metricas_completas(obs, sim):
    """Calcular todas las métricas de evaluación.

    Calcula NSE, KGE (con componentes r, alpha, beta), RMSE y PBIAS
    en una sola llamada para facilitar la evaluación completa del modelo.

    Parámetros
    ----------
    obs : ndarray
        Valores observados
    sim : ndarray
        Valores simulados

    Retorna
    -------
    dict
        Diccionario con todas las métricas:
        - NSE: Nash-Sutcliffe Efficiency
        - KGE: Kling-Gupta Efficiency
        - r: Correlación de Pearson
        - alpha: Ratio de variabilidades
        - beta: Ratio de medias
        - RMSE: Root Mean Square Error
        - PBIAS: Percent Bias

    Ejemplo
    -------
    >>> from numpy import array
    >>> obs = array([1.0, 2.0, 3.0, 4.0, 5.0])
    >>> sim = array([1.1, 2.1, 2.9, 4.2, 4.8])
    >>> m = metricas_completas(obs, sim)
    >>> print(f"NSE: {m['NSE']:.3f}, KGE: {m['KGE']:.3f}")
    """
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
