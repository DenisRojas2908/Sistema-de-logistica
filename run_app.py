#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Flask del sistema de logística
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cambiar al directorio de la aplicación
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar la aplicación
from app import app

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Logística FIIS SIE")
    print("📱 Abrir navegador en: http://localhost:5000")
    print("🔧 Modo desarrollo activado")
    print("📊 Presionar Ctrl+C para detener")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n⏹️  Sistema detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar el sistema: {str(e)}")
        sys.exit(1)