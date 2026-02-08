# Tarea 1: Modelo Hidrológico Conceptual de Dos Tanques

**Autor:** [Tu Nombre]
**Código:** [Tu código]
**Fecha:** Febrero 2026
**Curso:** Hidrología - Prof. Carlos David Hoyos

---

## Resumen (máx 200 palabras)

En este trabajo se desarrolló, calibró y validó un modelo hidrológico conceptual de dos tanques para la cuenca CAMELS 11180500. El modelo representa el almacenamiento de agua en el suelo (tanque 1) y en el acuífero (tanque 2), con 8 parámetros calibrables. Se utilizaron datos de precipitación y caudal del período 1980-2014, dividiendo en calibración (1990-2000) y validación (2000-2010). La calibración se realizó mediante evolución diferencial minimizando el Nash-Sutcliffe Efficiency (NSE). El modelo calibrado alcanzó un NSE de [X.XX] en calibración y [X.XX] en validación, demostrando [buena/regular/limitada] capacidad predictiva. Se identificaron limitaciones relacionadas con [mencionar limitaciones principales] y se proponen mejoras como [mencionar mejoras].

**Palabras clave:** modelado hidrológico, balance hídrico, calibración, CAMELS, dos tanques

---

## 1. Introducción

### 1.1 Contexto

Los modelos hidrológicos conceptuales son herramientas fundamentales para comprender y predecir el comportamiento de cuencas hidrográficas. El modelo de dos tanques es una aproximación simple pero efectiva que representa:

- **Procesos rápidos:** escorrentía directa y flujo superficial
- **Procesos lentos:** flujo base y descarga subterránea

### 1.2 Objetivos

1. Seleccionar una cuenca apropiada del dataset CAMELS
2. Implementar un modelo conceptual de dos tanques
3. Calibrar el modelo usando evolución diferencial
4. Evaluar el desempeño en un período independiente
5. Interpretar los parámetros desde una perspectiva física

---

## 2. Área de Estudio

### 2.1 Selección de la Cuenca

**Criterios de selección:**
- Área < 500 km²
- Fracción de nieve < 10% (preferible 0%)
- Datos completos 1980-2014

**Cuenca seleccionada: 11180500**

| Atributo | Valor |
|----------|-------|
| Área | 24.32 km² |
| Fracción de nieve | 0.00% |
| Precipitación media | 1.49 mm/día |
| Caudal medio | 0.281 mm/día |
| Ubicación | [Completar con datos reales] |
| Uso de suelo | [Completar] |
| Elevación media | [Completar] |

### 2.2 Justificación

La cuenca 11180500 fue seleccionada porque:
1. Cumple todos los criterios establecidos
2. No tiene influencia de nieve (0%), simplificando el modelo
3. Área pequeña (24 km²) permite respuesta hidrológica rápida
4. [Agregar más justificaciones con datos reales]

**Figura 1:** Mapa de ubicación y distribución de cuencas CAMELS
![](../figuras/exploracion_cuencas.png)

---

## 3. Datos

### 3.1 Dataset CAMELS

CAMELS (Catchment Attributes and Meteorology for Large-sample Studies) contiene:
- 671 cuencas en Estados Unidos
- Datos diarios 1980-2014 (35 años)
- Tres fuentes de precipitación: Daymet, Maurer, NLDAS
- Caudales observados (USGS)

### 3.2 Características de los Datos

**Tabla 1: Estadísticas por período**

| Período | P media (mm/d) | P máx | Q media (mm/d) | Q máx |
|---------|----------------|-------|----------------|-------|
| Completo | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| Calibración | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| Validación | [X.XX] | [X.XX] | [X.XX] | [X.XX] |

**Figura 2:** Series temporales de precipitación y caudal
![](../figuras/series_tiempo.png)

### 3.3 Comparación de Fuentes de Precipitación

**Tabla 2: Comparación Daymet vs Maurer vs NLDAS**

| Fuente | P media | Correlación | NSE |
|--------|---------|-------------|-----|
| Daymet | [X.XX] | [X.XX] | [X.XX] |
| Maurer | [X.XX] | [X.XX] | [X.XX] |
| NLDAS | [X.XX] | [X.XX] | [X.XX] |

**Conclusión:** Se seleccionó [Daymet/Maurer/NLDAS] por [razones].

---

## 4. Metodología

### 4.1 Estructura del Modelo

**Ecuaciones del balance hídrico:**

**Tanque 1 (Suelo):**
1. Evapotranspiración: $ET_t = ET_c + \beta \cdot P_t$
2. Precipitación neta: $P_{neta,t} = \max(P_t - ET_t, 0)$
3. Escorrentía directa: $Q_{directa,t} = \alpha_1 \cdot P_{neta,t}$
4. Almacenamiento: $S_1^* = S_{1,t-1} + (1-\alpha_1) \cdot P_{neta,t}$
5. Desborde: Si $S_1^* > D_1$: $Q_{desborde1,t} = S_1^* - D_1$
6. Salida lenta: $Q_{lento1,t} = k_1 \cdot S_1^*$

**Tanque 2 (Subterráneo):**
7. Flujo rápido: $Q_{rapido2,t} = \alpha_2 \cdot Q_{lento1,t}$
8. Almacenamiento: $S_2^* = S_{2,t-1} + (1-\alpha_2) \cdot Q_{lento1,t}$
9. Desborde: Si $S_2^* > D_2$: $Q_{desborde2,t} = S_2^* - D_2$
10. Salida lenta: $Q_{lento2,t} = k_2 \cdot S_2^*$

**Caudal total:**
$$Q_t = Q_{directa,t} + Q_{desborde1,t} + Q_{rapido2,t} + Q_{desborde2,t} + Q_{lento2,t}$$

**Figura 3:** Esquema conceptual del modelo
```
        P
        ↓
    [Tanque 1]
        ↓
    [Tanque 2]
        ↓
        Q
```

### 4.2 Parámetros del Modelo

| Parámetro | Descripción | Rango |
|-----------|-------------|-------|
| $ET_c$ | Evapotranspiración base | [0, 10] mm/d |
| $\beta$ | Fracción de ET adicional | [0, 1] |
| $\alpha_1$ | Escorrentía directa | [0, 1] |
| $D_1$ | Capacidad tanque 1 | [10, 500] mm |
| $k_1$ | Coef. liberación T1 | [0.001, 0.99] |
| $\alpha_2$ | Flujo rápido T2 | [0, 1] |
| $D_2$ | Capacidad tanque 2 | [10, 1000] mm |
| $k_2$ | Coef. liberación T2 | [0.001, 0.99] |

### 4.3 Función Objetivo

**Nash-Sutcliffe Efficiency (NSE):**

$$NSE = 1 - \frac{\sum_{t=1}^{n}(Q_{obs,t} - Q_{sim,t})^2}{\sum_{t=1}^{n}(Q_{obs,t} - \bar{Q}_{obs})^2}$$

- NSE = 1: ajuste perfecto
- NSE = 0: modelo = media
- NSE < 0: modelo peor que la media

### 4.4 Algoritmo de Optimización

**Evolución Diferencial (scipy.optimize.differential_evolution):**
- Población: 15 × 8 parámetros
- Iteraciones máximas: 100
- Estrategia: best1bin
- Tolerancia: 0.01

### 4.5 Períodos de Análisis

- **Calentamiento:** 365 días (excluidos de métricas)
- **Calibración:** 1990-01-01 a 2000-12-31 (10 años)
- **Validación:** 2000-01-01 a 2010-12-31 (10 años)

---

## 5. Resultados

### 5.1 Parámetros Calibrados

**Tabla 3: Parámetros óptimos y su interpretación**

| Parámetro | Valor | Interpretación Física |
|-----------|-------|----------------------|
| $ET_c$ | [X.XX] | [Interpretación] |
| $\beta$ | [X.XX] | [Interpretación] |
| $\alpha_1$ | [X.XX] | [Interpretación] |
| $D_1$ | [X.XX] | [Interpretación] |
| $k_1$ | [X.XX] | [Interpretación] |
| $\alpha_2$ | [X.XX] | [Interpretación] |
| $D_2$ | [X.XX] | [Interpretación] |
| $k_2$ | [X.XX] | [Interpretación] |

### 5.2 Desempeño del Modelo

**Tabla 4: Métricas de desempeño**

| Período | NSE | KGE | Sesgo (%) | RMSE |
|---------|-----|-----|-----------|------|
| Calibración | [X.XX] | [X.XX] | [X.XX] | [X.XX] |
| Validación | [X.XX] | [X.XX] | [X.XX] | [X.XX] |

**Figura 4:** Resultados de calibración
![](../figuras/calibracion.png)

**Figura 5:** Resultados de validación
![](../figuras/validacion.png)

### 5.3 Balance Hídrico

- Precipitación total: [X.XX] mm
- Caudal observado: [X.XX] mm
- ET estimada: [X.XX] mm
- Coeficiente de escorrentía: [X.XX]

---

## 6. Discusión

### 6.1 Interpretación de Parámetros

[Discutir significado físico de cada parámetro calibrado y si son razonables]

### 6.2 Desempeño del Modelo

[Analizar NSE, comparar calibración vs validación, identificar períodos bien/mal simulados]

### 6.3 Limitaciones

1. **Estructura simple:** Solo 2 tanques, no captura toda la complejidad
2. **ET simplificada:** No considera radiación, temperatura, humedad
3. **Parámetros constantes:** No variabilidad estacional
4. **Sin heterogeneidad espacial:** Cuenca tratada como unidad homogénea
5. [Agregar más según análisis]

### 6.4 Mejoras Propuestas

1. Incluir módulo de intercepción
2. ET Penman-Monteith en lugar de ET base
3. Calibración multi-objetivo (NSE + KGE)
4. Validación temporal (diferentes períodos climáticos)
5. [Agregar más]

---

## 7. Conclusiones

1. Se implementó exitosamente un modelo de dos tanques para la cuenca 11180500
2. El modelo alcanzó NSE = [X.XX], considerado [bueno/aceptable/pobre]
3. Los parámetros calibrados tienen significado físico razonable
4. Las principales limitaciones son [mencionar]
5. El modelo es útil para [mencionar aplicaciones]

---

## 8. Referencias

1. Nash, J.E. and Sutcliffe, J.V. (1970). River flow forecasting through conceptual models.
2. Addor, N. et al. (2017). The CAMELS data set. Hydrology and Earth System Sciences.
3. Gupta, H.V. et al. (2009). Decomposition of the mean squared error and NSE.

---

## Anexo: Uso de Herramientas de IA

**Herramientas utilizadas:**
- Claude Code (Anthropic)

**Tareas asistidas:**
1. Generación de código base para el modelo de dos tanques
2. Implementación de optimización con scipy
3. Creación de visualizaciones con matplotlib
4. [Describir cómo se usaron]

**Código revisado y entendido:** Sí
**Modificaciones realizadas:** [Describir modificaciones que hiciste]
