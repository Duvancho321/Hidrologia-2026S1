# Módulos Centrales de Hidrología

Este directorio contiene código reutilizable para todas las tareas del curso.

## Estructura

```
src/
├── __init__.py        # Inicialización del paquete
├── modelos.py         # Modelos hidrológicos conceptuales
├── metricas/          # Métricas de evaluación
│   ├── __init__.py
│   └── hidrologia.py
└── utils/             # Utilidades generales
    └── __init__.py
```

## Modelos (`modelos.py`)

Colección de modelos hidrológicos conceptuales implementados en el curso.

### DosTanques

Modelo de dos tanques en serie que representa almacenamiento de agua en suelo y sistema subterráneo.

**Parámetros:**
- `ETc`: Evapotranspiración constante [mm/día]
- `beta`: Coeficiente de interceptación [-]
- `alpha1`: Fracción de escorrentía directa del tanque 1 [-]
- `D1`: Capacidad máxima del tanque 1 [mm]
- `k1`: Coeficiente de descarga del tanque 1 [1/día]
- `alpha2`: Fracción de escorrentía rápida del tanque 2 [-]
- `D2`: Capacidad máxima del tanque 2 [mm]
- `k2`: Coeficiente de descarga del tanque 2 [1/día]

**Ejemplo:**
```python
from src.modelos import DosTanques
import numpy as np

# Crear modelo
modelo = DosTanques(ETc=2.0, beta=0.3, alpha1=0.1, D1=200.0,
                    k1=0.1, alpha2=0.3, D2=500.0, k2=0.01)

# Simular con precipitación
P = np.random.uniform(0, 10, 1000)  # mm/día
Q_sim, S1, S2 = modelo.run(P)

# También se puede crear desde array
params = [2.0, 0.3, 0.1, 200.0, 0.1, 0.3, 500.0, 0.01]
modelo = DosTanques.from_array(params)
```

## Métricas (`metricas/`)

Funciones para evaluar el desempeño de modelos hidrológicos.

### Métricas disponibles

- **`nse(obs, sim)`**: Nash-Sutcliffe Efficiency
  Rango: (-∞, 1], óptimo: 1

- **`kge(obs, sim)`**: Kling-Gupta Efficiency
  Retorna: (kge, r, alpha, beta)
  Rango: (-∞, 1], óptimo: 1

- **`rmse(obs, sim)`**: Root Mean Square Error
  Rango: [0, ∞), óptimo: 0

- **`pbias(obs, sim)`**: Percent Bias
  Rango: (-∞, ∞), óptimo: 0

- **`metricas_completas(obs, sim)`**: Calcula todas las métricas
  Retorna: dict con NSE, KGE, r, alpha, beta, RMSE, PBIAS

**Ejemplo:**
```python
from src.metricas import nse, kge, metricas_completas
import numpy as np

Q_obs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
Q_sim = np.array([1.1, 2.1, 2.9, 4.2, 4.8])

# Métricas individuales
nse_val = nse(Q_obs, Q_sim)
kge_val, r, alpha, beta = kge(Q_obs, Q_sim)

# Todas las métricas a la vez
metricas = metricas_completas(Q_obs, Q_sim)
print(f"NSE: {metricas['NSE']:.3f}")
print(f"KGE: {metricas['KGE']:.3f}")
print(f"RMSE: {metricas['RMSE']:.3f}")
```

## Utilidades (`utils/`)

Espacio reservado para funciones auxiliares comunes entre tareas.

## Añadir nuevos modelos o métricas

1. **Nuevo modelo**: Agregar clase al archivo `modelos.py` siguiendo el estilo de `DosTanques`
2. **Nueva métrica**: Agregar función a `metricas/hidrologia.py` y exportarla en `metricas/__init__.py`
3. **Nueva utilidad**: Crear funciones en `utils/` según sea necesario

## Mantenimiento

- Mantener docstrings completos (estilo NumPy)
- Incluir referencias bibliográficas para modelos/métricas
- Actualizar ejemplos cuando se añadan funciones
- Mantener tests unitarios (futuro)

---

**Autor:** Duvan Nieves
**Universidad Nacional de Colombia**
**Curso:** Hidrología 2026-1
