#!/bin/bash
# Convertir informe de Markdown a PDF

echo "Convirtiendo informe.md a PDF..."

# Opción 1: pandoc (recomendado)
if command -v pandoc &> /dev/null; then
    echo "Usando pandoc..."
    pandoc informe.md -o informe.pdf \
        --pdf-engine=xelatex \
        --variable geometry:margin=2.5cm \
        --variable fontsize=11pt \
        --variable linestretch=1.15 \
        --toc \
        --number-sections \
        -V lang=es-ES
    echo "✓ PDF generado: informe.pdf"
else
    echo "❌ pandoc no instalado"
    echo ""
    echo "Instalación:"
    echo "  conda install -y pandoc texlive-core -c conda-forge"
    echo ""
    echo "O usa alternativas:"
    echo "  1. Editar informe.md en Typora/Obsidian y exportar a PDF"
    echo "  2. Copiar contenido a Google Docs y descargar como PDF"
    echo "  3. Usar editor LaTeX online (Overleaf)"
fi
