"""
Módulo de Picking - Sistema de Logística FIIS SIE
Simula la preparación de pedidos con alta eficiencia
"""

import random
from .catalogos import dic_sku, dic_clientes

def asignar_picking(dia, pedidos, capacidad_picking=1500):
    """
    Asigna pedidos para picking.
    Ajuste: Alta eficiencia para mantener OTIF > 80%.
    """
    pedidos_preparados = {}
    pedidos_pendientes = {}
    unidades_preparadas = 0
    
    # AJUSTE 1: Eficiencia del personal (entre 90% y 110% de lo planeado)
    # Esto simula que a veces son más rápidos o un poco más lentos, pero eficientes.
    eficiencia_dia = random.uniform(0.90, 1.10)
    capacidad_real = capacidad_picking * eficiencia_dia

    # Convertir a lista y mezclar para no priorizar siempre a los mismos
    lista_pedidos = list(pedidos.items())
    random.shuffle(lista_pedidos)

    for pedido_id, pedido in lista_pedidos:
        total_unidades = sum(pedido['productos'].values())
        
        # Verificar si cabe en la capacidad del día
        if unidades_preparadas + total_unidades <= capacidad_real:
            
            # AJUSTE 2: Probabilidad de error operativo muy baja (2%)
            # Solo el 2% de los pedidos fallarán por errores humanos.
            # Esto garantiza que el OTIF se mantenga alto.
            if random.random() < 0.02: 
                # Simula un error (se queda pendiente)
                pedidos_pendientes[pedido_id] = pedido.copy()
                pedidos_pendientes[pedido_id]['total_unidades'] = total_unidades
            else:
                # Pedido preparado con éxito
                pedidos_preparados[pedido_id] = pedido.copy()
                pedidos_preparados[pedido_id]['total_unidades'] = total_unidades
                unidades_preparadas += total_unidades
        else:
            # No hay capacidad -> Backlog
            pedidos_pendientes[pedido_id] = pedido.copy()
            pedidos_pendientes[pedido_id]['total_unidades'] = total_unidades

    backlog = sum(p['total_unidades'] for p in pedidos_pendientes.values())
    
    # Calcular % de capacidad usada (evitando división por cero)
    capacidad_utilizada = (unidades_preparadas / capacidad_picking * 100) if capacidad_picking > 0 else 0

    return {
        'pedidos_preparados': pedidos_preparados,
        'pedidos_pendientes': pedidos_pendientes,
        'unidades_preparadas': unidades_preparadas,
        'backlog': backlog,
        'capacidad_utilizada': capacidad_utilizada
    }

def generar_hoja_picking(dia, pedidos_preparados):
    """
    Consolida los productos totales a recoger en el almacén
    """
    hoja_picking = {}
    
    for pedido in pedidos_preparados.values():
        for sku, cantidad in pedido['productos'].items():
            if sku not in hoja_picking:
                hoja_picking[sku] = 0
            hoja_picking[sku] += cantidad
    
    return hoja_picking

def mostrar_picking_dia(dia, resultados_picking):
    """
    Genera un resumen de texto para la consola
    """
    res = resultados_picking
    texto = [f"\n=== PICKING DÍA {dia} ==="]
    texto.append(f"Pedidos listos: {len(res['pedidos_preparados'])}")
    texto.append(f"Pendientes (Backlog): {len(res['pedidos_pendientes'])}")
    texto.append(f"Unidades procesadas: {res['unidades_preparadas']}")
    return "\n".join(texto)

def analizar_picking_por_zona(pedidos_preparados, dic_clientes):
    """
    Analiza la distribución de picking agrupada por zonas
    """
    picking_por_zona = {}
    
    for pedido in pedidos_preparados.values():
        cliente_id = pedido['cliente']
        # Protección por si el cliente no existe en el diccionario
        if cliente_id in dic_clientes:
            zona = dic_clientes[cliente_id]['zona']
        else:
            zona = "Sin Zona"
            
        if zona not in picking_por_zona:
            picking_por_zona[zona] = {}
            
        for sku, cantidad in pedido['productos'].items():
            if sku not in picking_por_zona[zona]:
                picking_por_zona[zona][sku] = 0
            picking_por_zona[zona][sku] += cantidad
            
    return picking_por_zona