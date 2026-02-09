"""Script de prueba para verificar módulos centrales

Este script verifica que los módulos centrales se importan correctamente.
Requiere tener instaladas las dependencias (numpy, scipy, pandas, matplotlib).

Ejecutar: python3 src/test_modulos.py
"""
import sys
from pathlib import Path

# Agregar raíz del proyecto al path
proyecto_raiz = Path(__file__).parent.parent
sys.path.insert(0, str(proyecto_raiz))

print("="*70)
print("VERIFICACIÓN DE MÓDULOS CENTRALES")
print("="*70)

# Test 1: Importar modelo
print("\n[1/3] Importando modelo DosTanques...")
try:
    from src.modelos import DosTanques
    print("✓ DosTanques importado correctamente")
except Exception as e:
    print(f"✗ Error importando DosTanques: {e}")
    sys.exit(1)

# Test 2: Importar métricas
print("\n[2/3] Importando métricas...")
try:
    from src.metricas import nse, kge, rmse, pbias, metricas_completas
    print("✓ Todas las métricas importadas correctamente")
    print("  - nse, kge, rmse, pbias, metricas_completas")
except Exception as e:
    print(f"✗ Error importando métricas: {e}")
    sys.exit(1)

# Test 3: Crear instancia del modelo
print("\n[3/3] Creando instancia del modelo...")
try:
    modelo = DosTanques(ETc=2.0, beta=0.3, alpha1=0.1, D1=200.0,
                        k1=0.1, alpha2=0.3, D2=500.0, k2=0.01)
    print("✓ Modelo creado correctamente")
    print(f"  Parámetros: {modelo.p}")

    # Crear desde array
    modelo2 = DosTanques.from_array([2.0, 0.3, 0.1, 200, 0.1, 0.3, 500, 0.01])
    print("✓ Modelo creado desde array correctamente")
except Exception as e:
    print(f"✗ Error creando modelo: {e}")
    sys.exit(1)

# Test 4: Simular (requiere numpy)
print("\n[Opcional] Simulando modelo...")
try:
    import numpy as np
    P = np.random.uniform(0, 10, 100)  # 100 días de precipitación
    Q, S1, S2 = modelo.run(P)
    print(f"✓ Simulación exitosa: Q.shape={Q.shape}")

    # Calcular métricas (simular Q_obs = Q_sim para prueba)
    Q_obs = Q + np.random.normal(0, 0.1, len(Q))
    metricas = metricas_completas(Q_obs, Q)
    print(f"✓ Métricas calculadas:")
    print(f"  NSE: {metricas['NSE']:.4f}")
    print(f"  KGE: {metricas['KGE']:.4f}")
    print(f"  RMSE: {metricas['RMSE']:.4f}")
except ImportError:
    print("⚠ NumPy no instalado - saltando simulación")
    print("  Instalar con: pip install numpy")
except Exception as e:
    print(f"✗ Error en simulación: {e}")

print("\n" + "="*70)
print("VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("="*70)
print("\nLos módulos centrales están listos para usar en todas las tareas.")
print("Ejemplo de uso:")
print("  from src.modelos import DosTanques")
print("  from src.metricas import metricas_completas")
