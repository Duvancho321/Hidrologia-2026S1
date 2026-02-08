# ✅ Checklist Final - Tarea 1

## 🎯 Objetivo
Entregar antes del **Martes 17 de Febrero de 2026, 23:59**

---

## 📊 Estado Actual

### ✅ Completado (con datos sintéticos)
- [x] Selección de cuenca (11180500)
- [x] Implementación del modelo de dos tanques
- [x] Calibración y validación
- [x] Gráficas generadas
- [x] Análisis preliminar

### ⚠️  Pendiente (IMPORTANTE)
- [ ] **Obtener datos reales de CAMELS** (ver sección 1)
- [ ] **Escribir informe final** (ver sección 2)
- [ ] **Preparar archivo de entrega** (ver sección 3)

---

## 1️⃣ OBTENER DATOS REALES DE CAMELS

### Opción A: Descarga Manual (Recomendado)

```bash
# 1. Ir a una de estas URLs:
# https://ral.ucar.edu/solutions/products/camels
# https://zenodo.org/records/15529996

# 2. Descargar:
#    - basin_timeseries_v1p2_modelOutput_daymet.zip (~1 GB)
#    - camels_attributes_v2.0.xlsx (opcional)

# 3. Descomprimir en ~/camels_data/

# 4. Actualizar ruta en codigo/02_preparar_datos.py línea 10:
CAMELS_DIR = Path.home() / 'camels_data'  # Ajustar tu ruta

# 5. Re-ejecutar todo
conda activate hidrologia
cd codigo/
./ejecutar_todo.sh
```

### Opción B: Script de Ayuda

```bash
python codigo/00_descargar_camels.py  # Ver instrucciones
```

### ✓ Verificar mejora de NSE
- Con datos reales, NSE debería ser > 0.5
- Si NSE < 0.3, revisar parámetros o estructura del modelo

---

## 2️⃣ ESCRIBIR INFORME (10 páginas máx)

### Template creado en: `informe/informe_template.md`

### Secciones Requeridas:

#### ✅ 1. Resumen (máx 200 palabras)
- Objetivo, metodología, resultados, conclusiones

#### ✅ 2. Introducción
- Contexto
- Objetivos específicos

#### ✅ 3. Área de Estudio
- Justificación de cuenca seleccionada
- Características (área, clima, topografía)

#### ✅ 4. Datos
- Descripción CAMELS
- Estadísticas por período
- Comparación fuentes de precipitación

#### ✅ 5. Metodología
- Ecuaciones del modelo
- Parámetros y rangos
- Función objetivo (NSE)
- Algoritmo de optimización

#### ✅ 6. Resultados
- Parámetros calibrados
- Métricas de desempeño (NSE, KGE, etc.)
- Gráficas (calibración, validación)
- Balance hídrico

#### ✅ 7. Discusión
- Interpretación física de parámetros
- Limitaciones del modelo
- Comparación calibración vs validación

#### ✅ 8. Conclusiones
- Resumen de hallazgos
- Aplicabilidad del modelo

#### ✅ 9. Anexo: Uso de IA
- Qué herramientas usaste (Claude Code)
- Cómo las usaste
- Qué código fue asistido y cómo lo revisaste

### Figuras Requeridas (mínimo):
- [ ] Mapa/distribución de cuencas
- [ ] Series temporales (P y Q)
- [ ] Resultados calibración
- [ ] Resultados validación
- [ ] Comparación fuentes precipitación (si aplica)

### Formato:
```bash
# Opción 1: LaTeX (opcional)
# Usa template en informe/informe_template.md como guía

# Opción 2: Word/LibreOffice
# Convierte a PDF antes de entregar

# Opción 3: Markdown → PDF
pandoc informe_template.md -o informe.pdf --pdf-engine=xelatex
```

---

## 3️⃣ PREPARAR ENTREGA

### Estructura Requerida:
```
apellido_nombre_tarea1.tar.gz
├── codigo/
│   ├── modelo.py
│   ├── calibrar.py
│   ├── utils.py
│   └── requirements.txt
├── datos/
│   ├── forzamiento.csv    # SOLO tu cuenca
│   ├── caudal.csv          # SOLO tu cuenca
│   └── atributos.csv       # SOLO tu cuenca
├── figuras/
│   ├── series_tiempo.png
│   ├── calibracion.png
│   ├── validacion.png
│   └── comparacion_precip.png (si aplica)
├── informe/
│   ├── informe.pdf
│   └── informe.tex (opcional)
└── README.md
```

### Ejecutar Script de Entrega:

```bash
# 1. Editar preparar_entrega.sh líneas 5-6:
APELLIDO="tu_apellido"
NOMBRE="tu_nombre"

# 2. Ejecutar
./preparar_entrega.sh

# 3. Verificar
# - Tamaño < 50 MB
# - Contiene todos los archivos
# - README.md completo
```

### ⚠️  IMPORTANTE:
- **NO incluir** todos los datos de CAMELS (solo tu cuenca)
- **Tamaño máximo:** 50 MB
- **Formato:** .tar.gz
- **Nombre:** apellido_nombre_tarea1.tar.gz

---

## 4️⃣ VERIFICACIÓN FINAL

### Antes de Entregar:

- [ ] Código corre sin errores
- [ ] NSE calibración > 0.5 (con datos reales)
- [ ] NSE validación razonable (± 0.1 del NSE calibración)
- [ ] Todas las figuras tienen títulos, ejes y leyendas
- [ ] Informe tiene máximo 10 páginas
- [ ] README.md explica cómo ejecutar
- [ ] Se documentó uso de herramientas IA
- [ ] Archivo < 50 MB
- [ ] Solo datos de TU cuenca (no todo CAMELS)

### Probar Archivo de Entrega:

```bash
# Extraer en directorio temporal
mkdir test_entrega
cd test_entrega
tar -xzf ../apellido_nombre_tarea1.tar.gz

# Verificar estructura
ls -R

# Probar ejecución
pip install -r codigo/requirements.txt
python codigo/calibrar.py

# Si funciona → LISTO PARA ENTREGAR
```

---

## 🚀 Resumen de Pasos

1. **Descargar CAMELS** → Re-ejecutar con datos reales
2. **Escribir informe** → Usar template, completar con resultados reales
3. **Preparar entrega** → Ejecutar `./preparar_entrega.sh`
4. **Verificar** → Extraer y probar que funcione
5. **Entregar** → Subir a plataforma antes del 17 de febrero

---

## 📞 Ayuda Adicional

### Si NSE es muy bajo (< 0.3):
```python
# Intentar con otra fuente de precipitación
# O ajustar límites de parámetros
# O verificar datos de entrada
```

### Si el modelo no converge:
```python
# Aumentar maxiter en differential_evolution
# O usar diferentes semillas (seed=)
# O verificar balance hídrico
```

### Si encuentras errores:
```bash
# Verificar ambiente conda activo
conda activate hidrologia

# Verificar dependencias
conda list

# Re-instalar si es necesario
conda install -y numpy pandas matplotlib scipy -c conda-forge
```

---

## 📅 Timeline Sugerido

| Días restantes | Tarea |
|----------------|-------|
| Hoy | Descargar CAMELS, re-ejecutar con datos reales |
| -3 días | Completar informe (primera versión) |
| -2 días | Revisar informe, ajustar figuras |
| -1 día | Preparar entrega, verificar |
| Día de entrega | Subir antes de 23:59 |

---

**¡Mucho éxito con la tarea! 🎓**
