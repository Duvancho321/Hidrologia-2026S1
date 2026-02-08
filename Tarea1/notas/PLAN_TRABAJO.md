# Plan de Trabajo - Tarea 1

## Cronograma Sugerido

**Fecha de entrega:** Martes 17 de Febrero de 2026

| Semana | Actividades | Entregables |
|--------|-------------|-------------|
| **Semana 1** | Exploración CAMELS y selección de cuenca | Cuenca seleccionada, datos descargados |
| **Semana 2** | Análisis exploratorio de datos | Gráficas y estadísticas básicas |
| **Semana 3** | Implementación del modelo | Código funcional del modelo |
| **Semana 4** | Calibración y validación | Parámetros óptimos, métricas |
| **Semana 5** | Análisis, informe y entrega | Informe completo |

## Progreso por Parte

### Parte 1: Exploración de CAMELS (10%)

**Objetivo:** Seleccionar una cuenca apropiada para el modelado.

#### Tareas
- [ ] Descargar dataset CAMELS desde Zenodo
- [ ] Explorar estructura de archivos
- [ ] Cargar atributos de las 671 cuencas
- [ ] Filtrar cuencas por criterios:
  - [ ] Área < 500 km²
  - [ ] Fracción de nieve < 10%
  - [ ] Datos completos 1980-2014
- [ ] Seleccionar cuenca final
- [ ] Documentar justificación de la selección

#### Tiempo estimado: 4-6 horas

#### Notas
- Usar `cuencas_validas.csv` como punto de partida
- Explorar al menos 3-5 cuencas candidatas
- Considerar ubicación geográfica y clima

---

### Parte 2: Exploración de Datos (20%)

**Objetivo:** Entender las características de los datos hidrológicos de la cuenca seleccionada.

#### Tareas
- [ ] Cargar datos de precipitación (3 fuentes)
- [ ] Cargar datos de caudal observado
- [ ] Graficar series temporales completas
- [ ] Calcular estadísticas básicas:
  - [ ] Media, mediana, desviación estándar
  - [ ] Máximos y mínimos
  - [ ] Percentiles (25, 50, 75)
- [ ] Comparar fuentes de precipitación:
  - [ ] Correlaciones entre fuentes
  - [ ] Diferencias en magnitud
  - [ ] Diferencias en timing
- [ ] Identificar períodos anómalos o datos faltantes
- [ ] Crear visualizaciones para el informe

#### Tiempo estimado: 6-8 horas

#### Notas
- Usar matplotlib o plotly para visualizaciones
- Guardar todas las figuras en alta resolución (300 dpi)
- Documentar unidades de medida

---

### Parte 3: Implementación del Modelo (25%)

**Objetivo:** Implementar un modelo hidrológico conceptual de dos tanques funcional.

#### Tareas
- [ ] Diseñar estructura de clases/funciones
- [ ] Implementar ecuaciones del balance hídrico:
  - [ ] Evapotranspiración
  - [ ] Escorrentía directa
  - [ ] Almacenamiento Tanque 1
  - [ ] Almacenamiento Tanque 2
  - [ ] Caudal total
- [ ] Implementar verificación de balance hídrico
- [ ] Crear función de ejecución del modelo
- [ ] Ejecutar con parámetros por defecto
- [ ] Graficar resultados preliminares
- [ ] Comparar con caudal observado
- [ ] Documentar código (docstrings)

#### Tiempo estimado: 10-12 horas

#### Parámetros por defecto sugeridos
```python
params_default = {
    'ETc': 2.0,      # mm/día
    'beta': 0.3,     # fracción
    'alpha1': 0.1,   # fracción
    'D1': 200.0,     # mm
    'k1': 0.1,       # 1/día
    'alpha2': 0.3,   # fracción
    'D2': 500.0,     # mm
    'k2': 0.01       # 1/día
}
```

#### Notas
- Asegurar que el código sea modular y reutilizable
- Validar que no haya valores negativos de almacenamiento
- Verificar conservación de masa

---

### Parte 4: Calibración (25%)

**Objetivo:** Encontrar los parámetros óptimos que mejor ajusten el modelo a los datos observados.

#### Tareas
- [ ] Implementar función objetivo (NSE)
- [ ] Implementar función objetivo (KGE) - opcional
- [ ] Definir límites de parámetros
- [ ] Configurar algoritmo de optimización (differential_evolution)
- [ ] Calibrar con período 1990-2000
- [ ] Guardar parámetros óptimos
- [ ] Evaluar en período de validación 2000-2010
- [ ] Reportar métricas de desempeño
- [ ] Graficar hidrogramas observados vs simulados
- [ ] **Extra (+10%):** Calibrar con las 3 fuentes de precipitación

#### Tiempo estimado: 8-10 horas (14-16 horas con extra)

#### Notas
- Excluir primeros 365 días (calentamiento)
- Guardar evolución de la calibración
- Considerar múltiples ejecuciones para verificar convergencia

---

### Parte 5: Análisis y Discusión (20%)

**Objetivo:** Interpretar resultados y proponer mejoras al modelo.

#### Tareas
- [ ] Interpretar físicamente cada parámetro calibrado
- [ ] Analizar sensibilidad de parámetros
- [ ] Discutir limitaciones del modelo:
  - [ ] Procesos no representados
  - [ ] Suposiciones simplificadas
  - [ ] Incertidumbre en datos
- [ ] Comparar desempeño calibración vs validación
- [ ] Identificar períodos mal simulados
- [ ] Proponer mejoras al modelo:
  - [ ] Procesos adicionales
  - [ ] Estructura alternativa
  - [ ] Fuentes de datos adicionales
- [ ] Conclusiones generales

#### Tiempo estimado: 6-8 horas

#### Notas
- Ser crítico pero constructivo
- Relacionar con literatura hidrológica
- Considerar aplicabilidad práctica

---

## Informe Final

### Estructura (Máximo 10 páginas)

1. **Resumen** (máx. 200 palabras)
   - Objetivo, metodología, resultados principales

2. **Introducción**
   - Contexto y objetivos
   - Importancia de modelado hidrológico

3. **Área de Estudio**
   - Descripción de la cuenca
   - Justificación de la selección

4. **Datos**
   - Descripción de CAMELS
   - Fuentes de precipitación
   - Procesamiento de datos

5. **Metodología**
   - Estructura del modelo
   - Ecuaciones del balance hídrico
   - Proceso de calibración
   - Métricas de evaluación

6. **Resultados**
   - Parámetros calibrados
   - Métricas de desempeño
   - Gráficas de series simuladas

7. **Discusión**
   - Interpretación de parámetros
   - Limitaciones del modelo
   - Comparación calibración vs validación

8. **Conclusiones**
   - Resumen de hallazgos
   - Lecciones aprendidas
   - Trabajo futuro

9. **Anexo: Uso de Herramientas de IA**
   - Qué herramientas se usaron
   - Cómo se usaron
   - Qué código fue asistido por IA

### Tiempo estimado: 10-12 horas

---

## Resumen de Tiempo Total

| Parte | Tiempo estimado |
|-------|-----------------|
| Parte 1: Exploración CAMELS | 4-6 horas |
| Parte 2: Exploración de datos | 6-8 horas |
| Parte 3: Implementación | 10-12 horas |
| Parte 4: Calibración | 8-10 horas (14-16 con extra) |
| Parte 5: Análisis | 6-8 horas |
| Informe | 10-12 horas |
| **Total** | **44-56 horas** (50-62 con extra) |

---

## Checklist de Entrega

### Archivos de Código
- [ ] `codigo/modelo.py` - Implementación del modelo
- [ ] `codigo/calibrar.py` - Script de calibración
- [ ] `codigo/utils.py` - Funciones auxiliares
- [ ] `codigo/requirements.txt` - Dependencias

### Archivos de Datos
- [ ] `datos/forzamiento.csv` - Precipitación y ET
- [ ] `datos/caudal.csv` - Caudal observado
- [ ] `datos/atributos.csv` - Características de la cuenca

### Figuras
- [ ] `figuras/series_tiempo.png` - Series temporales
- [ ] `figuras/calibracion.png` - Resultados calibración
- [ ] `figuras/validacion.png` - Resultados validación
- [ ] `figuras/comparacion_precip.png` - Si aplica

### Informe
- [ ] `informe/informe.pdf` - Informe final
- [ ] `informe/informe.tex` - Fuente LaTeX (opcional)

### Documentación
- [ ] `README.md` - Instrucciones de ejecución
- [ ] Resultados principales en README
- [ ] Documentación de herramientas de IA

### Compresión y Envío
- [ ] Archivo comprimido < 50 MB
- [ ] Nombre: `apellido_nombre_tarea1.tar.gz`
- [ ] Verificar que todo funciona después de descomprimir
- [ ] Enviar antes del martes 17 de febrero, 23:59

---

## Recursos y Referencias

### Documentación
- CAMELS: https://ral.ucar.edu/solutions/products/camels
- SciPy optimize: https://docs.scipy.org/doc/scipy/reference/optimize.html
- Matplotlib: https://matplotlib.org/stable/contents.html
- Pandas: https://pandas.pydata.org/docs/

### Papers Relevantes
- Nash-Sutcliffe (1970): Modelo conceptual de caudal
- Gupta et al. (2009): KGE efficiency

### Herramientas de IA
- Claude Code (este proyecto)
- GitHub Copilot (si se usa)
- ChatGPT (si se usa)

---

## Notas de Progreso

### Fecha: [YYYY-MM-DD]
**Actividad:**

**Logros:**

**Problemas encontrados:**

**Próximos pasos:**

---

### Fecha: [YYYY-MM-DD]
**Actividad:**

**Logros:**

**Problemas encontrados:**

**Próximos pasos:**
