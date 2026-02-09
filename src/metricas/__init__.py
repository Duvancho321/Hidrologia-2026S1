"""Métricas de evaluación hidrológica

Funciones para evaluar el desempeño de modelos hidrológicos.

__author__: "Duvan Nieves"
__copyright__: "UNAL"
"""
from .hidrologia import nse, kge, rmse, pbias, metricas_completas

__all__ = ['nse', 'kge', 'rmse', 'pbias', 'metricas_completas']
