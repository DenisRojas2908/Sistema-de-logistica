"""
Módulo de Picking - Sistema de Logística FIIS SIE
Corrección: Asegura que 'total_unidades' exista siempre.
"""
import random
from .catalogos import dic_sku, dic_clientes

def asignar_picking(dia, pedidos, capacidad_picking, inventario_disponible):
    """
    Asigna pedidos verificando tanto la mano de obra como el stock físico.
    """
    pedidos_preparados = {}
    pedidos_pendientes = {}
    unidades_preparadas = 0
    
    # Copia temporal para ir restando stock mientras asignamos
    stock_virtual = inventario_disponible.copy()
    
    # Eficiencia variable (90-110%)
    capacidad_real = capacidad_picking * random.uniform(0.90, 1.10)

    # Mezclar pedidos
    lista_pedidos = list(pedidos.items())
    random.shuffle(lista_pedidos)

    for pedido_id, pedido in lista_pedidos:
        # 1. CALCULAR TOTALES PRIMERO (Corrección del error KeyError)
        total_unidades = sum(pedido['productos'].values())
        
        # Creamos la copia del pedido y le pegamos la etiqueta YA MISMO
        pedido_procesado = pedido.copy()
        pedido_procesado['total_unidades'] = total_unidades
        
        # 2. FILTRO DE CAPACIDAD OPERATIVA
        if unidades_preparadas + total_unidades > capacidad_real:
            pedidos_pendientes[pedido_id] = pedido_procesado
            continue 

        # 3. FILTRO DE STOCK
        stock_suficiente = True
        for sku, cantidad in pedido['productos'].items():
            if stock_virtual.get(sku, 0) < cantidad:
                stock_suficiente = False
                break
        
        if not stock_suficiente:
            pedidos_pendientes[pedido_id] = pedido_procesado
            continue

        # 4. APROBADO
        # Restamos del stock virtual
        for sku, cantidad in pedido['productos'].items():
            stock_virtual[sku] -= cantidad
            
        # Simulación leve de error humano (2%)
        if random.random() < 0.02: 
            pedidos_pendientes[pedido_id] = pedido_procesado
        else:
            pedidos_preparados[pedido_id] = pedido_procesado
            unidades_preparadas += total_unidades

    backlog = sum(p['total_unidades'] for p in pedidos_pendientes.values())
    cap_util = (unidades_preparadas / capacidad_picking * 100) if capacidad_picking > 0 else 0

    return {
        'pedidos_preparados': pedidos_preparados,
        'pedidos_pendientes': pedidos_pendientes,
        'unidades_preparadas': unidades_preparadas,
        'backlog': backlog,
        'capacidad_utilizada': cap_util
    }

# Auxiliares
def generar_hoja_picking(dia, pedidos_preparados): return {} 
def mostrar_picking_dia(dia, res): return ""
def analizar_picking_por_zona(p, c): return {}