# Hidrología 2026-1

Repositorio del curso de Hidrología - Universidad Nacional de Colombia

**Profesor:** Carlos David Hoyos
**Estudiante:** Duvan Nieves

## Contenido

- [Tarea 1: Modelo Hidrológico Conceptual](./Tarea1/) - Fecha de entrega: 17 de Febrero 2026

## Estructura del Repositorio

```
Hidrologia-2026S1/
├── src/              # Módulos compartidos entre todas las tareas
│   ├── modelos.py    # Modelos hidrológicos (DosTanques, etc.)
│   ├── metricas/     # Métricas de evaluación (NSE, KGE, RMSE, PBIAS)
│   └── utils/        # Utilidades generales
├── Tarea1/           # Tarea 1: Modelo hidrológico de dos tanques
│   ├── enunciado/    # Documentos del enunciado
│   ├── codigo/       # Scripts específicos de la tarea
│   ├── datos/        # Datos de CAMELS
│   ├── figuras/      # Gráficas y visualizaciones
│   ├── informe/      # Informe final
│   └── notas/        # Notas y avances
└── README.md         # Este archivo
```

## Módulos Centrales

El directorio `src/` contiene código reutilizable entre tareas:

- **`modelos.py`**: Modelos hidrológicos conceptuales (DosTanques, etc.)
- **`metricas/`**: Funciones de evaluación hidrológica (NSE, KGE, RMSE, PBIAS)
- **`utils/`**: Funciones auxiliares comunes

### Uso de los módulos

```python
# Importar modelo
from src.modelos import DosTanques

# Importar métricas
from src.metricas import nse, kge, metricas_completas

# Usar modelo
modelo = DosTanques(ETc=2.0, beta=0.3, alpha1=0.1, D1=200,
                    k1=0.1, alpha2=0.3, D2=500, k2=0.01)
Q_sim, S1, S2 = modelo.run(P)

# Evaluar desempeño
metricas = metricas_completas(Q_obs, Q_sim)
print(f"NSE: {metricas['NSE']:.3f}, KGE: {metricas['KGE']:.3f}")
```

## Herramientas Utilizadas

- Python 3.8+
- NumPy, Pandas, Matplotlib, SciPy
- Claude Code (Anthropic)
- Git para control de versiones
