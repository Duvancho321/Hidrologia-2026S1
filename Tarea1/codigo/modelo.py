"""Modelo Hidrológico de Dos Tanques

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintaner__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Creación del modelo conceptual de dos tanques.
"""
from numpy import array, zeros, ndarray

class DosTanques:
    def __init__(self, ETc, beta, alpha1, D1, k1, alpha2, D2, k2):
        self.p = array([ETc, beta, alpha1, D1, k1, alpha2, D2, k2])

    def run(self, P, S1_0=0, S2_0=0):
        """Ejecutar modelo con precipitación P (array)"""
        n, S1, S2, Q = len(P), zeros(len(P)+1), zeros(len(P)+1), zeros(len(P))
        S1[0], S2[0] = S1_0, S2_0
        ETc, beta, alpha1, D1, k1, alpha2, D2, k2 = self.p

        for t in range(n):
            # Balance T1
            ET, Pneta = ETc + beta * P[t], max(P[t] - (ETc + beta * P[t]), 0)
            Qdir, S1_temp = alpha1 * Pneta, min(S1[t] + (1 - alpha1) * Pneta, D1)
            Qdes1, Qlento1 = max(S1[t] + (1 - alpha1) * Pneta - D1, 0), k1 * S1_temp
            S1[t+1] = S1_temp - Qlento1

            # Balance T2
            Qrap2, S2_temp = alpha2 * Qlento1, min(S2[t] + (1 - alpha2) * Qlento1, D2)
            Qdes2, Qlento2 = max(S2[t] + (1 - alpha2) * Qlento1 - D2, 0), k2 * S2_temp
            S2[t+1] = S2_temp - Qlento2

            Q[t] = Qdir + Qdes1 + Qrap2 + Qdes2 + Qlento2

        return Q, S1[1:], S2[1:]

    @staticmethod
    def from_array(params):
        return DosTanques(*params)
