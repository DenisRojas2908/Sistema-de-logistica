"""
Sistema de Logística FIIS SIE
Paquete principal para simulación y análisis de operaciones logísticas
"""

from .catalogos import dic_sku, dic_clientes, dic_vehiculos, inventario_inicial, punto_reposicion, lote_reposicion
from .demanda import simular_demanda, mostrar_simulacion, exportar_pedidos_tabla
from .inventario import reservar_y_actualizar, reponer_simple, procesar_dia_inventario
from .picking import asignar_picking, generar_hoja_picking, mostrar_picking_dia
from .transporte import planificar_rutas, mostrar_transporte_dia, generar_programa_transporte
from .indicadores import calcular_indicadores, mostrar_indicadores, calcular_indicadores_acumulados
from .alertas import generar_alertas, mostrar_alertas, generar_recomendaciones
from .reporte import reporte_logistica, exportar_datos_csv

__version__ = "1.0.0"
__author__ = "FIIS SIE"
__description__ = "Sistema de simulación logística para análisis de desempeño"