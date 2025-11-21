#!/bin/bash

# Script de instalación para Sistema de Logística FIIS SIE

echo "🚀 Instalando Sistema de Logística FIIS SIE"
echo "=========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instale Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "✅ Python $PYTHON_VERSION detectado"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación
echo "🔍 Verificando instalación..."
python3 -c "import flask; print('✅ Flask instalado correctamente')"
python3 -c "import jupyter; print('✅ Jupyter instalado correctamente')"

# Hacer ejecutables los scripts
chmod +x run_app.py
chmod +x install.sh

echo ""
echo "🎉 Instalación completada exitosamente!"
echo ""
echo "📋 Opciones de uso:"
echo "   1. Interfaz Web: python3 run_app.py"
echo "   2. Notebook Jupyter: jupyter notebook simulador.ipynb"
echo "   3. Uso directo: python3 -c 'from sistema import simular_demanda'"
echo ""
echo "🌐 Abrir navegador en: http://localhost:5000"
echo "📊 Presionar Ctrl+C para detener el servidor"