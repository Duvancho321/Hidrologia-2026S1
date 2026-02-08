# Instrucciones Detalladas - Tarea 1

## Resumen Ejecutivo

Desarrollar un modelo hidrológico conceptual de dos tanques, calibrarlo con datos reales de CAMELS y evaluar su desempeño.

## Filosofía de la Tarea

**"Es preferible construir un modelo simple que funcione y se entienda completamente, que usar un modelo complejo como caja negra."**

La simplicidad del modelo de dos tanques permite enfocarse en los conceptos fundamentales sin perderse en detalles computacionales.

## Métrica de Evaluación: NSE y KGE

### Nash-Sutcliffe Efficiency (NSE)

```
NSE = 1 - Σ(Qobs - Qsim)² / Σ(Qobs - Q̄obs)²
```

**Interpretación:**
- NSE = 1: Ajuste perfecto
- NSE = 0: El modelo es tan bueno como usar la media
- NSE < 0: El modelo es peor que usar la media

**Por qué usarlo:**
- Normalización: permite comparar entre cuencas
- Referencia clara: usar la media como baseline
- Sensibilidad a errores grandes (penaliza picos mal simulados)

### Kling-Gupta Efficiency (KGE)

```
KGE = 1 - √[(r-1)² + (α-1)² + (βKGE-1)²]
```

Donde:
- r: correlación
- α: variabilidad (σsim/σobs)
- βKGE: sesgo (μsim/μobs)

**Ventajas:**
- Descomposición explícita: separa timing, variabilidad y sesgo
- Balance: da peso igual a los tres componentes
- Diagnóstico: identifica qué aspecto necesita mejora

**Recomendación:**
Reportar ambas métricas. NSE es útil para comparación histórica, KGE proporciona mejor diagnóstico.

## Algoritmo de Optimización

Usar **Evolución Diferencial** de SciPy:

```python
from scipy.optimize import differential_evolution

def objetivo(params):
    q_sim = modelo.run(precip, params)
    obs = q_obs[365:]  # Excluir calentamiento
    sim = q_sim[365:]
    nse = 1 - sum((obs-sim)**2) / sum((obs-obs.mean())**2)
    return -nse  # Minimizar = Maximizar NSE

bounds = [(0,1), (0,1), (10,500), (0.001,0.99),
          (0,1), (10,1000), (0.001,0.99)]

result = differential_evolution(objetivo, bounds, maxiter=100)
```

## Balance Hídrico por Paso de Tiempo

Para cada día t, partiendo del almacenamiento del día anterior (S1,t-1, S2,t-1):

1. **Evapotranspiración:** ETt = ETc + β·Pt
2. **Precipitación neta:** Pneta,t = max(Pt - ETt, 0)
3. **Escorrentía directa:** Qdirecta,t = α1·Pneta,t
4. **Almacenamiento temporal T1:** S*t = S1,t-1 + (1-α1)·Pneta,t
5. **Desborde T1:** Si S*t > D1: Qdesborde1,t = S*t - D1, S*t = D1
6. **Salida lenta T1:** Qlento1,t = k1·S*1; S1,t = S*t - Qlento1,t
7. **Flujo rápido T2:** Qrapido2,t = α2·Qlento1,t
8. **Almacenamiento temporal T2:** S*2 = S2,t-1 + (1-α2)·Qlento1,t
9. **Desborde T2:** Si S*2 > D2: Qdesborde2,t = S*2 - D2, S*2 = D2
10. **Salida lenta T2:** Qlento2,t = k2·S*2; S2,t = S*2 - Qlento2,t
11. **Caudal total:** Qt = Qdirecta,t + Qdesborde1,t + Qrapido2,t + Qdesborde2,t + Qlento2,t

**Nota:** S* representa el almacenamiento intermedio dentro del mismo paso de tiempo, antes de aplicar la salida lenta.

## Criterios de Selección de Cuenca

1. **Área < 500 km²:** Cuencas pequeñas responden más rápido
2. **Fracción de nieve < 10% (preferible 0%):** Evitar procesos de nieve
3. **Datos completos:** Sin gaps significativos en precipitación y caudal

## Fuentes de Precipitación en CAMELS

| Fuente | Resolución | Descripción |
|--------|-----------|-------------|
| Daymet | 1 km | Interpolación de estaciones meteorológicas |
| Maurer | 1/8° (~12 km) | Datos históricos en una malla regular |
| NLDAS | 1/8° (~12 km) | North American Land Data Assimilation System |

**Recomendación:** Empezar con Daymet (mayor resolución), luego comparar.

## Esquema del Modelo de Dos Tanques

```
                    Precipitación (P)
                           ↓
                    ET = ETc + βP
                           ↓
        ┌─────────────────────────────────────┐
        │      Tanque 1 (Suelo)               │
        │      Profundidad: D1                │
←───────│      Almacenamiento: S1             │───────→
Escor.  │                                     │  Desborde
directa │            ↓ k1·S1                  │  (S1>D1)
α1·Pneta│                                     │
        └─────────────────────────────────────┘
                           ↓
        ┌─────────────────────────────────────┐
        │   Tanque 2 (Subterráneo)            │
        │   Profundidad: D2                   │
←───────│   Almacenamiento: S2                │───────→
Flujo   │                                     │  Desborde
rápido  │         ↓ k2·S2                     │  (S2>D2)
α2·entrada                                    │
        └─────────────────────────────────────┘
                           ↓
                 Caudal Total (Q)
```

## Errores Comunes a Evitar

1. **No excluir período de calentamiento:** Los primeros 365 días deben excluirse de las métricas
2. **Confundir minimización/maximización:** NSE se maximiza (minimizar -NSE)
3. **No validar balance hídrico:** Verificar que la masa se conserva
4. **Usar todos los datos de CAMELS:** Solo incluir la cuenca seleccionada
5. **No documentar el uso de IA:** Indicar qué herramientas se usaron y cómo

## Preguntas Frecuentes

### ¿Puedo usar otra cuenca que no cumpla todos los criterios?

Sí, pero debe justificar la selección y explicar cómo afecta al modelo.

### ¿Puedo usar otro algoritmo de optimización?

Sí, pero debe explicar por qué lo eligió y comparar con evolución diferencial.

### ¿Qué hago si mi NSE es muy bajo?

Un NSE ≥0.5 se considera aceptable. Si obtiene valores muy bajos, discuta las posibles causas:
- Datos de mala calidad
- Estructura del modelo inadecuada
- Parámetros mal calibrados
- Procesos no representados (nieve, glaciares, etc.)

### ¿Puedo modificar la estructura del modelo?

Sí, siempre y cuando describa claramente:
1. Qué cambió en la estructura o ecuaciones
2. La justificación física o hidrológica del cambio
3. Cómo afecta el número de parámetros
4. Comparar el desempeño del modelo modificado con el modelo base

## Recomendaciones de Trabajo

1. **Empezar simple:** Primero hacer funcionar el modelo base
2. **Validar paso a paso:** Verificar balance hídrico antes de calibrar
3. **Visualizar todo:** Graficar series, parámetros, sensibilidad
4. **Documentar durante:** No dejar la documentación para el final
5. **Usar control de versiones:** Commit frecuente con mensajes descriptivos

## Checklist Final

Antes de entregar, verificar:

- [ ] El código corre sin errores
- [ ] El balance hídrico se conserva
- [ ] Las gráficas tienen etiquetas, leyendas y unidades
- [ ] El informe tiene máximo 10 páginas
- [ ] Se reportan NSE de calibración y validación
- [ ] Se interpretan físicamente los parámetros
- [ ] Se documentan herramientas de IA usadas
- [ ] El archivo comprimido es < 50 MB
- [ ] El README explica cómo ejecutar el código
- [ ] Solo se incluyen datos de la cuenca seleccionada
