# Tarea 1: Modelo Hidrológico Conceptual

**Fecha de entrega:** Martes 17 de Febrero de 2026
**Valor:** 500 puntos
**Profesor:** Carlos David Hoyos

## Objetivo

Desarrollar, calibrar y validar un modelo hidrológico conceptual sencillo de dos tanques utilizando datos de CAMELS (Catchment Attributes and Meteorology for Large-sample Studies).

## Descripción del Modelo

Modelo conceptual de dos tanques conectados en serie:
- **Tanque 1 (Suelo):** Representa el almacenamiento en el suelo
- **Tanque 2 (Subterráneo):** Representa el agua subterránea

### Parámetros a Calibrar (8 parámetros)

| Parámetro | Descripción | Mín | Máx | Interpretación física |
|-----------|-------------|-----|-----|-----------------------|
| ETc | Evapotranspiración base | 0 | 10 mm/día | Pérdida diaria constante por evaporación |
| β | Fracción de ET de P | 0 | 1 | Proporción adicional de P que se evapora |
| α1 | Escorrentía directa | 0 | 1 | Fracción de P que escurre inmediatamente |
| D1 | Profundidad tanque 1 | 10 | 500 mm | Capacidad de almacenamiento del suelo |
| k1 | Coef. liberación T1 | 0.001 | 0.99 | Velocidad de drenaje del suelo |
| α2 | Flujo rápido T2 | 0 | 1 | Fracción de flujo rápido subterráneo |
| D2 | Profundidad tanque 2 | 10 | 1000 mm | Capacidad del acuífero |
| k2 | Coef. liberación T2 | 0.001 | 0.99 | Velocidad de descarga del acuífero |

## Tareas a Realizar

### ✅ Parte 1: Exploración de CAMELS (10%)
- [ ] Descargar datos de CAMELS
- [ ] Explorar atributos de las 671 cuencas
- [ ] Seleccionar una cuenca que cumpla:
  - Área menor a 500 km²
  - Fracción de nieve menor a 10% (preferible 0%)
  - Datos completos de precipitación y caudal
- [ ] Comentar la selección de la cuenca

### 📊 Parte 2: Exploración de Datos (20%)
- [ ] Graficar series de tiempo de precipitación y caudal
- [ ] Calcular estadísticas básicas (media, desviación, máximos)
- [ ] Comparar las tres fuentes de precipitación (Daymet, Maurer, NLDAS)

### 💻 Parte 3: Implementación del Modelo (25%)
- [ ] Implementar el modelo de dos tanques en Python
- [ ] Verificar el balance hídrico
- [ ] Ejecutar el modelo con parámetros por defecto
- [ ] Graficar resultados del modelo no calibrado

### 🎯 Parte 4: Calibración (25%)
- [ ] Implementar la función objetivo (NSE)
- [ ] Calibrar el modelo usando al menos una fuente de precipitación
- [ ] Reportar los parámetros óptimos encontrados
- [ ] Evaluar el modelo en el período de validación
- [ ] **Opcional (+10% extra):** Calibrar con las tres fuentes y comparar

### 📝 Parte 5: Análisis y Discusión (20%)
- [ ] Interpretar físicamente los parámetros calibrados
- [ ] Discutir las limitaciones del modelo
- [ ] Comparar desempeño en calibración vs validación
- [ ] Proponer mejoras al modelo

## Períodos de Análisis

- **Calentamiento:** Primeros 365 días (excluir de métricas)
- **Calibración:** 1990-2000 (10 años)
- **Validación:** 2000-2010 (10 años)

## Estructura de Carpetas

```
Tarea1/
├── enunciado/
│   └── tarea1_enunciado.pdf    # Documento con instrucciones completas
├── codigo/
│   ├── modelo.py               # Modelo de dos tanques
│   ├── calibrar.py             # Script de calibración
│   ├── utils.py                # Funciones auxiliares
│   └── requirements.txt        # Dependencias Python
├── datos/
│   ├── cuencas_validas.csv     # Cuencas que cumplen criterios
│   ├── forzamiento.csv         # Datos meteorológicos (a generar)
│   ├── caudal.csv              # Datos de caudal (a generar)
│   └── atributos.csv           # Atributos de cuenca (a generar)
├── figuras/
│   ├── series_tiempo.png       # Series temporales
│   ├── calibracion.png         # Resultados calibración
│   ├── validacion.png          # Resultados validación
│   └── comparacion_precip.png  # Comparación fuentes (si aplica)
├── informe/
│   ├── informe.pdf             # Informe final
│   └── informe.tex             # Fuente LaTeX (opcional)
├── notas/
│   ├── INSTRUCCIONES.md        # Resumen de instrucciones
│   └── PLAN_TRABAJO.md         # Plan de trabajo y progreso
└── README.md                   # Este archivo
```

## Recursos

- **Datos CAMELS:** https://ral.ucar.edu/solutions/products/camels
- **Repositorio Zenodo:** https://zenodo.org/records/15529996
- **SciPy Optimization:** https://docs.scipy.org/doc/scipy/reference/optimize.html
- **Nash-Sutcliffe:** Nash, J.E. and Sutcliffe, J.V. (1970). River flow forecasting through conceptual models.

## Herramientas de IA Utilizadas

- Claude Code (Anthropic) - Asistente de programación

## Instalación y Ejecución

```bash
# Crear ambiente conda
conda create -n hidrologia python=3.10 -y
conda activate hidrologia
conda install -y numpy pandas matplotlib scipy pyarrow -c conda-forge

# Opción 1: Ejecutar todo el flujo completo (primera vez)
cd codigo/
./ejecutar_todo.sh

# Opción 2: Solo análisis (si ya tienes datos procesados)
./ejecutar_solo_analisis.sh

# Opción 3: Paso a paso
python 01_explorar_cuencas.py         # Seleccionar cuenca
python 02_preparar_datos.py           # Preparar datos
python 03_calibrar.py                 # Calibrar modelo
python 04_analisis.py                 # Análisis básico
python 05_analisis_avanzado.py        # Análisis avanzado (KGE, sensibilidad)
python 06_comparar_fuentes.py         # Comparar fuentes de precipitación
```

## Resultados Principales

- **NSE calibración:** 0.0635 (datos sintéticos)
- **NSE validación:** 0.0640 (datos sintéticos)
- **Nota:** NSE bajo debido a datos sintéticos. Con datos reales de CAMELS se esperan valores > 0.5

## Cuenca Seleccionada

- **ID:** 11180500
- **Área:** 24.32 km²
- **Fracción de nieve:** 0.00% (sin nieve)
- **Precipitación media:** 1.49 mm/día
- **Caudal medio:** 0.281 mm/día
- **Justificación:** Cumple todos los criterios (área < 500 km², sin nieve, datos completos)

## Parámetros Calibrados

| Parámetro | Valor | Interpretación |
|-----------|-------|----------------|
| ETc | 0.000 mm/d | Evapotranspiración base muy baja |
| β | 0.932 | Alta fracción de P que se evapora |
| α1 | 0.000 | Baja escorrentía directa |
| D1 | 101.4 mm | Capacidad del suelo pequeña |
| k1 | 0.059 | Drenaje del suelo lento |
| α2 | 0.760 | Alto flujo rápido subterráneo |
| D2 | 408.8 mm | Capacidad del acuífero pequeña |
| k2 | 0.002 | Descarga del acuífero lenta |

## Notas Importantes

- NO incluir todos los datos de CAMELS en la entrega
- Solo incluir datos de la cuenca seleccionada en formato CSV
- El archivo comprimido no debe exceder 50 MB
- Usar asistentes de IA está permitido y recomendado
- Documentar qué herramientas se usaron y cómo
