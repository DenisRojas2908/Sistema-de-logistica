# Sistema de Simulación Logística FIIS SIE

## Descripción

Sistema modular de simulación y análisis de operaciones logísticas para LIA S.A.C., empresa de distribución y transporte de productos de maquillaje.

## Características

- ✅ **Simulación de Demanda**: Generación automática de pedidos por cliente y zona
- ✅ **Control de Inventario**: Gestión de stock y reposición automática
- ✅ **Operaciones de Picking**: Preparación de pedidos con capacidad limitada
- ✅ **Planificación de Transporte**: Asignación óptima de rutas y vehículos
- ✅ **Indicadores KPI**: OTIF, Fill Rate, Backlog Rate, Productividad, Utilización de Flota
- ✅ **Sistema de Alertas**: Notificaciones automáticas para desviaciones
- ✅ **Reportes Consolidados**: Análisis completo con recomendaciones
- ✅ **Interfaz Web**: Dashboard interactivo para monitoreo en tiempo real

## Arquitectura

```
logistica_sim/
├── sistema/                 # Módulos principales
│   ├── __init__.py         # Paquete principal
│   ├── catalogos.py        # Catálogos de productos, clientes, vehículos
│   ├── demanda.py          # Simulación de demanda
│   ├── inventario.py       # Control de inventario
│   ├── picking.py          # Operaciones de picking
│   ├── transporte.py       # Planificación de transporte
│   ├── indicadores.py      # Cálculo de KPIs
│   ├── alertas.py          # Sistema de alertas
│   └── reporte.py          # Generación de reportes
├── templates/              # Interfaz web
│   └── index.html         # Dashboard principal
├── app.py                 # Backend Flask (API REST)
├── simulador.ipynb        # Notebook de demostración
├── requirements.txt       # Dependencias
└── README.md             # Documentación
```

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar el sistema**:

### Opción A: Interfaz Web
```bash
python app.py
# Abrir navegador en http://localhost:5000
```

### Opción B: Notebook Jupyter
```bash
jupyter notebook simulador.ipynb
```

### Opción C: Uso directo en Python
```python
from sistema import simular_demanda, procesar_dia_inventario, asignar_picking
# ... usar funciones según necesidad
```

## Uso

### Interfaz Web

1. **Panel de Control**:
   - Configurar días de simulación (1-30)
   - Ajustar capacidad de picking (500-5000 unidades/día)
   - Ejecutar simulación

2. **Dashboard**:
   - Indicadores de desempeño en tiempo real
   - Sistema de alertas con recomendaciones
   - Tabla de pedidos procesados
   - Reporte completo descargable

### Notebook de Demostración

El notebook `simulador.ipynb` incluye:
- Explicación detallada de cada módulo
- Ejecución paso a paso de la simulación
- Visualizaciones de tendencias
- Análisis de resultados
- Conclusiones y recomendaciones

## Catálogos Configurados

### Productos (SKU)
- P001: Lápiz Labial
- P002: Base
- P003: Rubor
- P004: Máscara de Pestañas
- P005: Sombras de Ojos

### Clientes
- C01: AVON (Zona Este)
- C02: ESIKA (Zona Norte)
- C03: ARUMA (Zona Sur)
- C04: INKAFARMA (Zona Oeste)
- C05: FALABELLA (Zona Centro)

### Vehículos
- V01: Camioneta (100 unidades, S/ 4.5/km)
- V02: Camión (120 unidades, S/ 5.0/km)
- V03: Furgoneta (80 unidades, S/ 3.8/km)
- V04: Camión Grande (150 unidades, S/ 6.2/km)
- V05: Camioneta (90 unidades, S/ 4.0/km)

## Indicadores KPI

- **OTIF**: On Time In Full (% pedidos completos y a tiempo)
- **Fill Rate**: Unidades entregadas / Unidades solicitadas × 100
- **Backlog Rate**: Unidades pendientes / Unidades solicitadas × 100
- **Productividad Picking**: Unidades preparadas por hora
- **Utilización de Flota**: Capacidad utilizada / Capacidad disponible × 100

## Ejemplos de Uso

### Simulación Básica
```python
# Simular 7 días de operación
pedidos = simular_demanda(7, dic_clientes, dic_sku)

# Procesar primer día
resultado_inventario = procesar_dia_inventario(pedidos['Dia_1'], inventario_inicial)
resultado_picking = asignar_picking(1, pedidos['Dia_1'])
resultado_transporte = planificar_rutas(1, resultado_picking['pedidos_preparados'])
```

### Análisis de Indicadores
```python
# Calcular indicadores
indicadores = calcular_indicadores(
    pedidos_recibidos=len(pedidos_dia),
    pedidos_preparados=resultado_picking['pedidos_preparados'],
    pedidos_pendientes=resultado_picking['pedidos_pendientes'],
    unidades_preparadas=resultado_picking['unidades_preparadas'],
    unidades_solicitadas=total_solicitadas,
    resultados_transporte=resultado_transporte
)
```

### Generación de Alertas
```python
# Generar alertas automáticas
alertas = generar_alertas(indicadores)
for alerta in alertas:
    print(f"{alerta['tipo']}: {alerta['mensaje']}")
```

## Características Técnicas

- **Backend**: Flask (Python) con API REST
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **Visualizaciones**: Matplotlib (Notebook Jupyter)
- **Arquitectura**: Modular y escalable
- **Base de Datos**: En memoria (para demo)
- **CORS**: Habilitado para integraciones

## Requisitos del Sistema

- Python 3.8+
- Flask 2.3+
- Jupyter Notebook (opcional)
- Navegador web moderno
- 2GB RAM mínimo

## Contribuciones

Este sistema fue desarrollado como proyecto académico para el curso de FIIS SIE. 

## Licencia

Proyecto académico - Uso educativo.

## Contacto

Para consultas sobre el sistema, contactar al equipo de desarrollo FIIS SIE.

---

**¡Sistema listo para uso! 🚀**

El sistema de simulación logística FIIS SIE proporciona una herramienta completa para:
- Analizar y optimizar operaciones logísticas
- Identificar cuellos de botella
- Mejorar la eficiencia operativa
- Tomar decisiones basadas en datos
- Planificar capacidad y recursos