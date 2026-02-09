"""Modelos Hidrológicos Conceptuales

Colección de modelos hidrológicos para el curso de Hidrología UNAL.
Cada modelo es una clase independiente con métodos estándar de simulación.

__author__: "Duvan Nieves"
__copyright__: "UNAL"
__version__: "1.0.0"
__maintainer__: "Duvan Nieves"
__email__: "dnieves@unal.edu.co"
__status__: "Production"
__changes__:
   - [2026-02-07]: Creación del modelo DosTanques.
   - [2026-02-09]: Migración a módulo central src/modelos.py
"""
from numpy import array, zeros, ndarray


class DosTanques:
    """Modelo hidrológico conceptual de dos tanques en serie.

    Parámetros
    ----------
    ETc : float
        Evapotranspiración constante [mm/día]
    beta : float
        Coeficiente de interceptación [-]
    alpha1 : float
        Fracción de escorrentía directa del tanque 1 [-]
    D1 : float
        Capacidad máxima del tanque 1 [mm]
    k1 : float
        Coeficiente de descarga del tanque 1 [1/día]
    alpha2 : float
        Fracción de escorrentía rápida del tanque 2 [-]
    D2 : float
        Capacidad máxima del tanque 2 [mm]
    k2 : float
        Coeficiente de descarga del tanque 2 [1/día]

    Atributos
    ---------
    p : ndarray
        Vector de parámetros del modelo [ETc, beta, alpha1, D1, k1, alpha2, D2, k2]
    """

    def __init__(self, ETc, beta, alpha1, D1, k1, alpha2, D2, k2):
        """Inicializar modelo con parámetros."""
        self.p = array([ETc, beta, alpha1, D1, k1, alpha2, D2, k2])

    def run(self, P, S1_0=0, S2_0=0):
        """Ejecutar simulación del modelo.

        Parámetros
        ----------
        P : ndarray
            Serie de precipitación [mm/día]
        S1_0 : float, opcional
            Almacenamiento inicial del tanque 1 [mm] (default: 0)
        S2_0 : float, opcional
            Almacenamiento inicial del tanque 2 [mm] (default: 0)

        Retorna
        -------
        Q : ndarray
            Caudal simulado [mm/día]
        S1 : ndarray
            Serie de almacenamiento del tanque 1 [mm]
        S2 : ndarray
            Serie de almacenamiento del tanque 2 [mm]
        """
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
        """Crear instancia del modelo desde array de parámetros.

        Parámetros
        ----------
        params : array-like
            Vector [ETc, beta, alpha1, D1, k1, alpha2, D2, k8]

        Retorna
        -------
        DosTanques
            Instancia del modelo inicializada
        """
        return DosTanques(*params)
