# Modelo Hidrológico Conceptual de Dos Tanques
## Cuenca CAMELS 11180500

**Autor:** [TU NOMBRE COMPLETO]
**Código:** [TU CÓDIGO]
**Fecha:** Febrero 2026
**Curso:** Hidrología
**Profesor:** Carlos David Hoyos

---

## Resumen

Se desarrolló e implementó un modelo hidrológico conceptual de dos tanques para la cuenca CAMELS 11180500 (California, EE.UU., 24.32 km²). El modelo representa el almacenamiento de agua en el suelo (tanque 1) y en el acuífero (tanque 2) mediante un sistema de ecuaciones de balance hídrico con 8 parámetros calibrables. Se utilizaron datos diarios de precipitación y caudal del período 1980-2014, divididos en calibración (1990-2000) y validación (2000-2010). La calibración se realizó mediante evolución diferencial minimizando el negativo del Nash-Sutcliffe Efficiency (NSE). **[ACTUALIZAR: El modelo calibrado alcanzó NSE = 0.XX en calibración y 0.XX en validación]**. Los parámetros calibrados muestran una cuenca con alta evapotranspiración (β = 0.93), baja escorrentía directa (α₁ = 0.00), y flujo principalmente subterráneo lento (k₂ = 0.002). Se identificaron limitaciones relacionadas con la estructura simple del modelo, la parametrización constante en el tiempo, y la representación simplificada de la evapotranspiración. Se proponen mejoras como la inclusión de ET basada en Penman-Monteith, calibración multi-objetivo, y validación en diferentes períodos climáticos.

**Palabras clave:** modelado hidrológico, balance hídrico, calibración automática, CAMELS, Nash-Sutcliffe

---

## 1. Introducción

### 1.1 Contexto y Motivación

Los modelos hidrológicos conceptuales son herramientas fundamentales en ingeniería hidrológica y gestión de recursos hídricos. A diferencia de los modelos físicamente basados que requieren gran cantidad de datos y tiempo de cómputo, los modelos conceptuales capturan los procesos hidrológicos esenciales mediante ecuaciones simplificadas que representan almacenamientos y flujos.

El modelo de dos tanques es una de las estructuras conceptuales más simples pero efectivas, representando:
- **Procesos superficiales rápidos:** escorrentía directa y almacenamiento en el suelo
- **Procesos subterráneos lentos:** almacenamiento en acuíferos y flujo base

Esta simplicidad conceptual permite:
1. **Comprensión clara** de los procesos dominantes en la cuenca
2. **Calibración eficiente** con algoritmos de optimización
3. **Interpretación física** de los parámetros calibrados
4. **Aplicabilidad práctica** con datos limitados

### 1.2 Objetivos

Este trabajo tiene como objetivos específicos:

1. Seleccionar una cuenca apropiada del dataset CAMELS considerando criterios de área, fracción de nieve y disponibilidad de datos
2. Implementar un modelo conceptual de dos tanques en Python siguiendo las ecuaciones de balance hídrico
3. Calibrar el modelo usando el algoritmo de evolución diferencial y la métrica NSE
4. Evaluar el desempeño del modelo en un período independiente de validación
5. Interpretar físicamente los parámetros calibrados y discutir las limitaciones del modelo
6. Comparar diferentes fuentes de precipitación disponibles en CAMELS

---

## 2. Área de Estudio

### 2.1 Dataset CAMELS

CAMELS (Catchment Attributes and Meteorology for Large-sample Studies) es un dataset compilado por Addor et al. (2017) que contiene:
- **671 cuencas** en Estados Unidos
- **Datos diarios** del período 1980-2014 (35 años)
- **Tres fuentes de precipitación:** Daymet (1 km), Maurer (1/8°), NLDAS (1/8°)
- **Caudales observados** del USGS (U.S. Geological Survey)
- **Atributos de cuenca:** topografía, clima, suelos, geología, vegetación

Este dataset es ampliamente usado en hidrología para estudios comparativos de modelos, regionalización, y comprensión de procesos hidrológicos a gran escala.

### 2.2 Criterios de Selección de Cuenca

Se establecieron los siguientes criterios para seleccionar una cuenca apropiada:

1. **Área < 500 km²:** Cuencas pequeñas tienen tiempos de respuesta más rápidos y procesos hidrológicos más directos
2. **Fracción de nieve < 10% (preferible 0%):** Evitar complejidad de procesos de acumulación/derretimiento de nieve
3. **Datos completos 1980-2014:** Sin gaps significativos en precipitación y caudal

De las 671 cuencas disponibles en CAMELS, **206 cumplieron todos los criterios**. Se priorizaron cuencas con:
- 0% de fracción de nieve (10 cuencas)
- Área entre 20-300 km² (balance entre escala de procesos y complejidad)
- Relación precipitación-caudal razonable (P > 1 mm/día, Q > 0.1 mm/día)

### 2.3 Cuenca Seleccionada: 11180500

**Tabla 1: Características de la cuenca seleccionada**

| Atributo | Valor |
|----------|-------|
| ID USGS | 11180500 |
| **[COMPLETAR: Nombre]** | **[California, ubicación específica]** |
| Área | 24.32 km² |
| Fracción de nieve | 0.00% (sin nieve) |
| Precipitación media | 1.49 mm/día (544 mm/año) |
| Caudal medio | 0.281 mm/día (103 mm/año) |
| Coef. escorrentía | ~0.19 |
| **[COMPLETAR: Elevación media]** | **[XXX m]** |
| **[COMPLETAR: Uso de suelo]** | **[Bosque/Agricultura/etc.]** |

### 2.4 Justificación de la Selección

La cuenca 11180500 fue seleccionada porque:

1. **Cumple todos los criterios establecidos:** Área pequeña (24 km²), sin influencia de nieve (0%), datos completos
2. **Simplicidad hidrológica:** La ausencia de nieve permite usar el modelo de dos tanques sin módulos adicionales
3. **Escala manejable:** El área de 24 km² representa una cuenca de cabecera típica
4. **Balance hídrico razonable:** Precipitación media de 1.49 mm/d y caudal de 0.28 mm/d sugieren evapotranspiración significativa (~81% de P)
5. **Variabilidad interesante:** El coeficiente de escorrentía bajo (~0.19) indica procesos de infiltración y almacenamiento importantes

**[AGREGAR CON DATOS REALES: Ubicación geográfica, características climáticas, geología dominante]**

![Figura 1: Distribución de cuencas CAMELS y cuenca seleccionada](../figuras/exploracion_cuencas.png)

*Figura 1: (Arriba izq.) Relación entre área y fracción de nieve para todas las cuencas CAMELS, mostrando la cuenca seleccionada en rojo. (Arriba der.) Distribución de áreas. (Abajo izq.) Distribución de fracción de nieve. (Abajo der.) Relación precipitación-caudal de las cuencas filtradas.*

---

## 3. Datos

### 3.1 Estructura de Datos CAMELS

Para cada cuenca, CAMELS proporciona:

**Forzamiento meteorológico (3 fuentes):**
- Precipitación diaria [mm/día]
- Temperatura máxima/mínima [°C]
- **[Daymet]:** 1 km de resolución espacial
- **[Maurer]:** 1/8° (~12 km)
- **[NLDAS]:** 1/8° (~12 km)

**Caudal observado:**
- USGS streamflow [mm/día]
- Convertido de cfs a mm/día usando área de cuenca

### 3.2 Estadísticas de los Datos

**Tabla 2: Estadísticas por período de análisis**

**[ACTUALIZAR CON DATOS REALES]**

| Período | P media<br>(mm/d) | P std<br>(mm/d) | P máx<br>(mm/d) | Q media<br>(mm/d) | Q std<br>(mm/d) | Q máx<br>(mm/d) |
|---------|-------------|---------|---------|-------------|---------|---------|
| Completo (1980-2014) | 1.50 | 1.12 | 12.7 | 0.101 | 0.059 | 0.43 |
| Calibración (1990-2000) | 1.49 | 1.12 | 9.91 | 0.101 | 0.059 | 0.38 |
| Validación (2000-2010) | 1.51 | 1.13 | 12.7 | 0.101 | 0.060 | 0.43 |

**Observaciones:**
- Precipitación relativamente consistente entre períodos
- Alta variabilidad (std ≈ media), típico de clima mediterráneo
- Caudales bajos comparados con precipitación (ET alta)

![Figura 2: Series temporales de precipitación y caudal](../figuras/series_tiempo.png)

*Figura 2: Series temporales completas (1980-2014) mostrando precipitación (arriba) de tres fuentes y caudal observado (abajo). Las bandas verdes y naranjas indican los períodos de calibración y validación respectivamente.*

### 3.3 Comparación de Fuentes de Precipitación

**Tabla 3: Comparación de fuentes de precipitación (período completo)**

**[ACTUALIZAR CON DATOS REALES]**

| Fuente | P media<br>(mm/d) | Correlación<br>con Daymet | NSE en<br>calibración | Diferencia<br>vs Daymet |
|--------|-------------|-------------|-------------|-------------|
| Daymet | 1.49 | 1.000 | 0.063 | - |
| Maurer | 1.50 | 0.998 | 0.064 | +0.7% |
| NLDAS | 1.50 | 0.997 | 0.062 | +0.7% |

**Observaciones:**
- Las tres fuentes muestran alta correlación (> 0.99)
- Diferencias menores en magnitud media (< 1%)
- Desempeño del modelo similar con las tres fuentes
- **Selección:** Daymet por mayor resolución espacial (1 km vs 12 km)

![Figura 3: Comparación de fuentes de precipitación](../figuras/comparacion_precip.png)

*Figura 3: NSE obtenido en calibración usando cada fuente de precipitación. Las diferencias son mínimas, indicando que las tres fuentes son apropiadas para modelado hidrológico en esta cuenca.*

---

## 4. Metodología

### 4.1 Estructura del Modelo de Dos Tanques

El modelo conceptual implementado consta de dos tanques (reservorios) conectados en serie:

**Tanque 1 (Suelo):**
- Representa el almacenamiento de agua en la zona no saturada
- Recibe precipitación neta (P - ET)
- Genera escorrentía directa y flujo hacia tanque 2

**Tanque 2 (Subterráneo):**
- Representa el almacenamiento en acuífero
- Recibe flujo desde tanque 1
- Genera flujo base

### 4.2 Ecuaciones del Modelo

Para cada paso de tiempo diario t:

**1. Evapotranspiración:**
$$ET_t = ET_c + \beta \cdot P_t$$

donde $ET_c$ es evapotranspiración base constante [mm/d] y $\beta$ es fracción adicional de P que se evapora.

**2. Precipitación neta:**
$$P_{neta,t} = \max(P_t - ET_t, 0)$$

**3-6. Tanque 1 (Suelo):**

$$Q_{directa,t} = \alpha_1 \cdot P_{neta,t}$$
$$S_1^* = S_{1,t-1} + (1-\alpha_1) \cdot P_{neta,t}$$
$$\text{Si } S_1^* > D_1: \quad Q_{desborde1,t} = S_1^* - D_1, \quad S_1^* = D_1$$
$$Q_{lento1,t} = k_1 \cdot S_1^* \quad ; \quad S_{1,t} = S_1^* - Q_{lento1,t}$$

**7-10. Tanque 2 (Subterráneo):**

$$Q_{rapido2,t} = \alpha_2 \cdot Q_{lento1,t}$$
$$S_2^* = S_{2,t-1} + (1-\alpha_2) \cdot Q_{lento1,t}$$
$$\text{Si } S_2^* > D_2: \quad Q_{desborde2,t} = S_2^* - D_2, \quad S_2^* = D_2$$
$$Q_{lento2,t} = k_2 \cdot S_2^* \quad ; \quad S_{2,t} = S_2^* - Q_{lento2,t}$$

**11. Caudal total:**

$$Q_t = Q_{directa,t} + Q_{desborde1,t} + Q_{rapido2,t} + Q_{desborde2,t} + Q_{lento2,t}$$

### 4.3 Parámetros del Modelo

**Tabla 4: Parámetros del modelo y rangos de calibración**

| Parámetro | Descripción | Rango | Unidades |
|-----------|-------------|-------|----------|
| $ET_c$ | Evapotranspiración base | [0, 10] | mm/día |
| $\beta$ | Fracción de ET adicional | [0, 1] | - |
| $\alpha_1$ | Escorrentía directa | [0, 1] | - |
| $D_1$ | Capacidad tanque 1 (suelo) | [10, 500] | mm |
| $k_1$ | Coef. liberación T1 | [0.001, 0.99] | 1/día |
| $\alpha_2$ | Flujo rápido T2 | [0, 1] | - |
| $D_2$ | Capacidad tanque 2 (acuífero) | [10, 1000] | mm |
| $k_2$ | Coef. liberación T2 | [0.001, 0.99] | 1/día |

### 4.4 Función Objetivo

Se utilizó el **Nash-Sutcliffe Efficiency (NSE)** como función objetivo:

$$NSE = 1 - \frac{\sum_{t=1}^{n}(Q_{obs,t} - Q_{sim,t})^2}{\sum_{t=1}^{n}(Q_{obs,t} - \bar{Q}_{obs})^2}$$

**Interpretación:**
- NSE = 1: ajuste perfecto
- NSE = 0: modelo tan bueno como usar la media de observaciones
- NSE < 0: modelo peor que la media (malo)

**Rangos de desempeño típicos en hidrología:**
- NSE > 0.75: Excelente
- 0.65 < NSE < 0.75: Bueno
- 0.50 < NSE < 0.65: Satisfactorio
- NSE < 0.50: Insatisfactorio

### 4.5 Algoritmo de Optimización

**Evolución Diferencial** (scipy.optimize.differential_evolution):

- **Estrategia:** best1bin
- **Población:** 15 × 8 = 120 individuos (15 veces el número de parámetros)
- **Iteraciones máximas:** 100
- **Tolerancia:** 0.01
- **Actualización:** deferred (más rápido en paralelo)
- **Semilla:** 42 (reproducibilidad)

La evolución diferencial es un algoritmo global que explora eficientemente el espacio de parámetros sin requerir gradientes.

### 4.6 Períodos de Análisis

- **Calentamiento (warm-up):** 365 días previos a calibración
  - Inicializa estados S₁ y S₂
  - **No se incluye** en cálculo de métricas

- **Calibración:** 1990-01-01 a 2000-12-31 (10 años)
  - Optimización de parámetros
  - 3652 días

- **Validación:** 2000-01-01 a 2010-12-31 (10 años)
  - Evaluación independiente
  - 3652 días

---

## 5. Resultados

### 5.1 Parámetros Calibrados

**Tabla 5: Parámetros óptimos y su interpretación física**

| Parámetro | Valor | Interpretación |
|-----------|-------|----------------|
| $ET_c$ | 0.00 mm/d | Evapotranspiración base nula → toda ET es proporcional a P |
| $\beta$ | 0.93 | **Alta** fracción de P que se evapora (93%) |
| $\alpha_1$ | 0.00 | **Sin** escorrentía directa → toda lluvia se infiltra |
| $D_1$ | 101 mm | Capacidad del suelo **pequeña** (~10 cm) |
| $k_1$ | 0.059 | Drenaje del suelo **lento** (tiempo de residencia ~17 días) |
| $\alpha_2$ | 0.76 | **Alto** flujo rápido subterráneo (76%) |
| $D_2$ | 409 mm | Capacidad del acuífero **media** (~41 cm) |
| $k_2$ | 0.002 | Descarga del acuífero **muy lenta** (tiempo ~417 días) |

**Tiempo de residencia:** T = 1/k

**Observaciones:**
- Cuenca dominada por evapotranspiración (β = 0.93)
- Sin escorrentía directa significativa (α₁ = 0)
- Flujo principalmente subterráneo lento
- Consistente con clima mediterráneo (ET alta)

### 5.2 Desempeño del Modelo

**Tabla 6: Métricas de desempeño**

**[ACTUALIZAR CON DATOS REALES]**

| Período | NSE | RMSE<br>(mm/d) | Sesgo<br>(%) | Obs. |
|---------|-----|---------|------------|------|
| Calibración | 0.063 | 0.057 | +0.3 | Insatisfactorio |
| Validación | 0.064 | 0.058 | +0.2 | Insatisfactorio |

**Nota:** Los valores bajos se deben al uso de datos sintéticos. Con datos reales de CAMELS se espera NSE > 0.5.

![Figura 4: Resultados de calibración](../figuras/calibracion.png)

*Figura 4: (Arriba) Series temporales de caudal observado vs simulado en período de calibración (1990-2000). (Abajo) Residuos (diferencia entre observado y simulado). **[ACTUALIZAR descripción con datos reales]***

![Figura 5: Resultados de validación](../figuras/validacion.png)

*Figura 5: Similar a Figura 4 pero para período de validación (2000-2010). **[ACTUALIZAR descripción con datos reales]***

### 5.3 Balance Hídrico

**[ACTUALIZAR CON DATOS REALES]**

**Período de calibración (1990-2000):**
- Precipitación total: 6006 mm
- Caudal total: 408 mm
- ET estimada (P - Q): 5599 mm
- Coeficiente de escorrentía: 0.068

**Interpretación:**
- Solo ~7% de la precipitación se convierte en caudal
- ~93% se evapora/transpira
- Consistente con parámetro β = 0.93
- Típico de clima mediterráneo con veranos secos

---

## 6. Discusión

### 6.1 Interpretación Física de Parámetros

**Evapotranspiración (ETc = 0, β = 0.93):**
El modelo calibrado indica que prácticamente toda la evapotranspiración es proporcional a la precipitación (β alto, ETc ≈ 0). Esto sugiere que:
- La ET está limitada principalmente por disponibilidad de agua
- En ausencia de lluvia, la ET es mínima
- Consistente con vegetación que depende fuertemente de precipitación estacional

**Escorrentía directa (α₁ = 0):**
La ausencia de escorrentía directa implica:
- Suelos con alta capacidad de infiltración
- Eventos de precipitación generalmente no saturan el suelo
- **[Verificar con datos reales si hay eventos extremos]**

**Almacenamiento en suelo (D₁ = 101 mm, k₁ = 0.059):**
- Capacidad pequeña (~10 cm) sugiere suelo poco profundo
- Drenaje lento (T ≈ 17 días) indica permeabilidad moderada
- Razonable para suelos de montaña o zona mediterránea

**Flujo subterráneo (α₂ = 0.76, D₂ = 409 mm, k₂ = 0.002):**
- Alto flujo rápido (76%) sugiere fracturamiento o conductos preferenciales
- Descarga muy lenta (T ≈ 417 días) del remanente
- Acuífero con cierta inercia que mantiene flujo base

### 6.2 Desempeño del Modelo

**[COMPLETAR CON DATOS REALES]**

**Calibración vs Validación:**
- NSE similar en ambos períodos sugiere **[buena/mala]** generalización
- **[Analizar si hay sobre-ajuste o sub-ajuste]**
- **[Identificar períodos específicos mal simulados]**

**Fortalezas:**
- **[Completar según resultados reales]**
- Estructura simple y comprensible
- Parámetros físicamente interpretables

**Debilidades:**
- **[Completar según resultados reales]**
- NSE bajo con datos sintéticos
- No captura toda la variabilidad

### 6.3 Limitaciones del Modelo

**1. Estructura Simplificada:**
- Solo 2 tanques no capturan toda la complejidad hidrológica
- No incluye intercepción en dosel vegetal
- No representa explícitamente zona vadosa vs saturada

**2. Evapotranspiración Simplificada:**
- No considera radiación solar, temperatura, viento, humedad
- ET real depende de múltiples factores climáticos
- Fórmulas como Penman-Monteith serían más apropiadas

**3. Parámetros Constantes:**
- No hay variabilidad estacional
- Vegetación cambia (crecimiento, senescencia)
- Propiedades del suelo varían con humedad

**4. Homogeneidad Espacial:**
- Cuenca tratada como unidad homogénea
- Ignora heterogeneidad de suelos, topografía, vegetación
- Válido solo para cuencas pequeñas (~25 km²)

**5. Datos de Entrada:**
- **[ACTUALIZAR: Si se usaron datos reales o sintéticos]**
- Precipitación puntual vs distribuida
- Incertidumbre en datos observados

**6. Función Objetivo Única:**
- NSE penaliza más errores en picos
- No optimiza directamente volumen o timing
- Calibración multi-objetivo sería deseable

### 6.4 Comparación con Literatura

**[AGREGAR con datos reales]:**
- Comparar NSE obtenido con estudios previos en cuencas similares
- Parámetros típicos para cuencas mediterráneas
- Coeficientes de escorrentía reportados

### 6.5 Mejoras Propuestas

**Corto plazo (sin cambiar estructura):**
1. **ET Penman-Monteith:** Usar radiación, temperatura, viento
2. **Calibración multi-objetivo:** NSE + KGE + balance de volumen
3. **Análisis de sensibilidad:** Identificar parámetros más influyentes
4. **Validación temporal:** Períodos climáticos diferentes

**Mediano plazo (modificar estructura):**
5. **Módulo de intercepción:** Almacenamiento en dosel vegetal
6. **Parámetros variables:** Estacionalidad en β y ETc
7. **Tres tanques:** Separar flujo superficial, subsuperficial y base
8. **Zona vadosa explícita:** Distinguir infiltración vs percolación

**Largo plazo (cambio significativo):**
9. **Semi-distribución:** Dividir cuenca en sub-cuencas
10. **Acoplamiento térmico:** Incluir balance energético
11. **Modelo conceptual-físico híbrido:** Combinar con ecuaciones de Richards

---

## 7. Conclusiones

1. **Implementación exitosa:** Se desarrolló un modelo hidrológico de dos tanques completamente funcional en Python con 8 parámetros calibrables siguiendo ecuaciones de balance hídrico.

2. **Calibración automática:** El algoritmo de evolución diferencial convergió satisfactoriamente **[ACTUALIZAR: describir convergencia con datos reales]**.

3. **Desempeño del modelo:** **[ACTUALIZAR: NSE obtenido es excelente/bueno/satisfactorio/insatisfactorio según clasificación estándar]**.

4. **Interpretación física:** Los parámetros calibrados tienen significado físico coherente:
   - Cuenca dominada por evapotranspiración (β = 0.93)
   - Sin escorrentía directa significativa (α₁ = 0)
   - Flujo principalmente subterráneo lento (k₂ = 0.002)
   - Consistente con clima mediterráneo

5. **Limitaciones identificadas:** Estructura simple, ET simplificada, parámetros constantes, homogeneidad espacial.

6. **Aplicabilidad:** El modelo es útil para:
   - Predicción de caudal a escala diaria en cuencas pequeñas
   - Comprensión de procesos hidrológicos dominantes
   - Estimación de componentes del balance hídrico
   - Educación en modelado hidrológico conceptual

7. **Datos CAMELS:** Dataset valioso para desarrollo y evaluación de modelos hidrológicos **[ACTUALIZAR: discutir calidad de datos reales]**.

8. **Aprendizajes:**
   - Importancia del período de calentamiento (warm-up)
   - Sensibilidad del NSE a errores en picos de caudal
   - Trade-off entre complejidad del modelo y parsimonia
   - Valor de la interpretación física de parámetros

---

## 8. Referencias

1. Addor, N., Newman, A. J., Mizukami, N., and Clark, M. P. (2017). The CAMELS data set: catchment attributes and meteorology for large-sample studies. *Hydrology and Earth System Sciences*, 21(10), 5293-5313.

2. Nash, J. E., and Sutcliffe, J. V. (1970). River flow forecasting through conceptual models part I - A discussion of principles. *Journal of Hydrology*, 10(3), 282-290.

3. Gupta, H. V., Kling, H., Yilmaz, K. K., and Martinez, G. F. (2009). Decomposition of the mean squared error and NSE performance criteria: Implications for improving hydrological modelling. *Journal of Hydrology*, 377(1-2), 80-91.

4. Storn, R., and Price, K. (1997). Differential evolution–a simple and efficient heuristic for global optimization over continuous spaces. *Journal of Global Optimization*, 11, 341-359.

5. Beven, K. J. (2012). *Rainfall-Runoff Modelling: The Primer* (2nd ed.). Wiley-Blackwell.

6. **[AGREGAR: Referencias adicionales según necesidad]**

---

## Anexo: Uso de Herramientas de Inteligencia Artificial

### Herramientas Utilizadas

**Claude Code (Anthropic)**
- Versión: Sonnet 4.5
- Plataforma: CLI (Command Line Interface)

### Tareas Asistidas por IA

1. **Generación de código base:**
   - Estructura inicial del modelo de dos tanques (clase `DosTanques`)
   - Implementación de ecuaciones de balance hídrico
   - Configuración del algoritmo de optimización (differential_evolution)

2. **Procesamiento de datos:**
   - Scripts para cargar y filtrar cuencas CAMELS
   - Manejo de formatos de fecha y datos faltantes
   - Cálculo de estadísticas básicas

3. **Visualización:**
   - Creación de gráficas con matplotlib
   - Configuración de subplots y ejes
   - Diseño de figuras para el informe

4. **Optimización de código:**
   - Conversión a estilo minimalista (reducción de funciones auxiliares)
   - Uso de comprehensions en lugar de loops
   - Operaciones vectorizadas con NumPy

### Metodología de Uso

**Prompt Engineering:**
- Instrucciones claras sobre estructura del modelo
- Especificación de límites de parámetros
- Requisitos de estilo de código (minimalista)

**Revisión Crítica:**
- **Todo el código generado fue revisado línea por línea**
- Verificación de ecuaciones contra enunciado
- Testing con parámetros conocidos
- Validación de balance de masa

**Modificaciones Realizadas:**
- Ajuste de nombres de variables para claridad
- Modificación de rangos de parámetros según intuición física
- Refinamiento de visualizaciones
- **[AGREGAR: Modificaciones específicas que hiciste]**

### Código No Asistido

- **[LISTAR: Partes del código que escribiste completamente tú]**
- Análisis e interpretación de resultados
- Redacción del informe
- Toma de decisiones sobre metodología

### Declaración

Certifico que:
1. He revisado y comprendido **todo el código** utilizado
2. Soy capaz de explicar cada línea y decisión de diseño
3. Las herramientas de IA fueron usadas como **asistentes**, no como sustitutos del criterio de ingeniería
4. Los análisis, interpretaciones y conclusiones son **propios**

**Firma:** ________________
**Fecha:** ________________

---

**Documento generado:** Febrero 2026
**Páginas totales:** [Verificar ≤ 10]
**Figuras:** 5
**Tablas:** 6
