# ✅ Checklist para Completar el Informe

## 📄 Archivo: `informe/informe.md`

El borrador está **90% completo**. Solo necesitas:

---

## 🔴 CRÍTICO - Actualizar con Datos Reales

Busca en el informe los marcadores **[ACTUALIZAR]** y **[COMPLETAR]**:

### 1. Resumen (pág. 1)
- [ ] Actualizar NSE calibración y validación
- [ ] Revisar descripción de resultados

### 2. Área de Estudio (pág. 2-3)
- [ ] **[COMPLETAR: Nombre]** de la cuenca (buscar en USGS)
- [ ] **[COMPLETAR: Elevación media]**
- [ ] **[COMPLETAR: Uso de suelo]**
- [ ] Agregar descripción de ubicación geográfica

### 3. Datos (pág. 4-5)
- [ ] **Tabla 2:** Actualizar estadísticas con datos reales
- [ ] **Tabla 3:** Actualizar comparación de fuentes
- [ ] Actualizar descripciones de figuras

### 4. Resultados (pág. 6-7)
- [ ] **Tabla 6:** Actualizar NSE, RMSE, sesgo
- [ ] Actualizar balance hídrico
- [ ] Actualizar descripciones de Figuras 4 y 5

### 5. Discusión (pág. 7-9)
- [ ] Completar análisis de desempeño
- [ ] Identificar períodos mal simulados
- [ ] Comparar con literatura (opcional)

### 6. Anexo (pág. 10)
- [ ] **[LISTAR]** código que escribiste tú
- [ ] **[AGREGAR]** modificaciones específicas

---

## 📝 Información Personal

Al inicio del documento, reemplazar:

```markdown
**Autor:** [TU NOMBRE COMPLETO]
**Código:** [TU CÓDIGO]
```

Con tus datos reales.

---

## 🎨 Convertir a PDF

### Opción 1: pandoc (Recomendado)

```bash
# Instalar pandoc si no lo tienes
conda activate hidrologia
conda install -y pandoc texlive-core -c conda-forge

# Convertir
cd informe/
./convertir_a_pdf.sh
```

### Opción 2: Typora / Obsidian / Mark Text

1. Abrir `informe.md` en el editor
2. Archivo → Exportar → PDF
3. Guardar como `informe.pdf`

### Opción 3: Google Docs

1. Copiar contenido de `informe.md`
2. Pegar en Google Docs
3. Formato → Markdown (extensión) o formato manual
4. Archivo → Descargar → PDF

### Opción 4: Overleaf (LaTeX)

1. Copiar contenido
2. Convertir Markdown → LaTeX
3. Compilar en Overleaf

---

## 📊 Verificar Figuras

Todas las figuras deben estar en `../figuras/`:

- [x] exploracion_cuencas.png
- [x] series_tiempo.png
- [x] calibracion.png
- [x] validacion.png
- [x] comparacion_precip.png

**Acción:** Verifica que las figuras tengan buena calidad (300 dpi).

---

## 📏 Verificar Extensión

**Límite:** Máximo 10 páginas

**Actual:** ~10-11 páginas (depende del formato)

**Si excede:**
- Reducir tamaño de figuras
- Condensar texto en Discusión
- Eliminar redundancias

**Si es muy corto:**
- Expandir interpretación de parámetros
- Agregar más análisis en Discusión
- Incluir más referencias

---

## 🔍 Revisión Final

Antes de entregar:

- [ ] Todas las ecuaciones se ven correctamente
- [ ] Todas las tablas están completas
- [ ] Todas las figuras tienen caption
- [ ] Referencias citadas en el texto
- [ ] Sin marcadores [ACTUALIZAR] o [COMPLETAR]
- [ ] Ortografía y gramática revisadas
- [ ] Numeración de secciones correcta
- [ ] Máximo 10 páginas
- [ ] Formato profesional

---

## 💡 Tips

### Ecuaciones LaTeX en PDF

Si usas pandoc, las ecuaciones se renderizan automáticamente.

Si usas Word/Docs, puedes:
1. Usar editor de ecuaciones
2. O insertar como imágenes (menos recomendado)

### Calidad de Figuras

Para incluir en LaTeX/pandoc:
```markdown
![Título](../figuras/nombre.png){ width=100% }
```

Para ajustar tamaño en diferentes formatos.

### Sección de Referencias

Agregar más si:
- Comparaste con otros estudios
- Usaste metodologías específicas
- Citaste características de la cuenca

---

## ⏱️ Tiempo Estimado

- Completar campos [ACTUALIZAR]: **30-60 min**
- Buscar info de cuenca: **15-30 min**
- Revisar y pulir: **30-60 min**
- Convertir a PDF: **15 min**
- **Total:** ~2-3 horas

---

## 🎯 Cuando Tengas Datos Reales

1. Re-ejecutar calibración:
   ```bash
   python 03_calibrar.py
   ```

2. Verificar nuevos resultados en `datos/parametros_optimos.csv`

3. Actualizar TODAS las secciones marcadas

4. Regenerar informe

¡Listo para entregar!
