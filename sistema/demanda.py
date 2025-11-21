"""
Módulo de Demanda - Sistema de Logística FIIS SIE
Simula la llegada de pedidos diarios por cliente
"""

import random
from .catalogos import dic_clientes, dic_sku

def simular_demanda(n_dias, dic_clientes, dic_sku):
    """
    Simula la llegada de pedidos diarios por cliente.
    Ajuste: Demanda moderada (12-20 pedidos) para realismo en stock.
    """
    pedidos_por_dia = {}
    
    for dia in range(1, n_dias + 1):
        pedidos_dia = {}
        
        # AJUSTE: Cantidad de pedidos moderada para que el stock baje gradualmente
        # Antes era muy alto, ahora permite ver la reposición funcionar.
        n_pedidos = random.randint(12, 20) 
        
        for i in range(n_pedidos):
            # Generar ID único por día
            pedido_id = f"{(dia-1)*20 + i + 1:03d}"
            
            cliente_id = random.choice(list(dic_clientes.keys()))
            
            # Cada pedido tiene entre 1 y 3 tipos de productos
            n_productos = random.randint(1, 3)
            productos = {}
            
            for _ in range(n_productos):
                sku = random.choice(list(dic_sku.keys()))
                # Cantidad por producto (5 a 40 unidades)
                cantidad = random.randint(5, 40) 
                productos[sku] = cantidad
            
            pedidos_dia[pedido_id] = {
                'cliente': cliente_id,
                'productos': productos,
                'fecha': dia,
                'zona': dic_clientes[cliente_id]['zona']
            }
        
        pedidos_por_dia[f"Dia_{dia}"] = pedidos_dia
    
    return pedidos_por_dia

def mostrar_simulacion(pedidos_por_dia, dia_especifico=None):
    """
    Muestra la simulación de pedidos de manera formateada en consola
    """
    if dia_especifico:
        dias_a_mostrar = [f"Dia_{dia_especifico}"] if f"Dia_{dia_especifico}" in pedidos_por_dia else []
    else:
        dias_a_mostrar = list(pedidos_por_dia.keys())
    
    resultado = []
    
    for dia_key in dias_a_mostrar:
        pedidos_dia = pedidos_por_dia[dia_key]
        resultado.append(f"\n=== Simulación de pedidos - {dia_key.replace('_', ' ')} ===")
        
        total_unidades = 0
        for pedido_id, pedido in pedidos_dia.items():
            cliente_nombre = dic_clientes[pedido['cliente']]['nombre']
            resultado.append(f"\nPedido {pedido_id} → {cliente_nombre}")
            
            for sku, cantidad in pedido['productos'].items():
                resultado.append(f"  • {sku}: {cantidad} unds")
                total_unidades += cantidad
                
        resultado.append(f"\nTotal unidades día: {total_unidades}")
    
    return "\n".join(resultado)

def exportar_pedidos_tabla(pedidos_por_dia):
    """
    Exporta los pedidos en formato lista de diccionarios para el Frontend
    """
    tabla_pedidos = []
    
    for dia_key, pedidos_dia in pedidos_por_dia.items():
        dia_num = dia_key.split('_')[1]
        
        for pedido_id, pedido in pedidos_dia.items():
            for sku, cantidad in pedido['productos'].items():
                tabla_pedidos.append({
                    'Fecha': f"Día {dia_num}",
                    'Pedido_ID': pedido_id,
                    'Cliente': pedido['cliente'],
                    'Nombre_Cliente': dic_clientes[pedido['cliente']]['nombre'],
                    'Producto': sku,
                    'Nombre_Producto': dic_sku[sku]['nombre'],
                    'Cantidad': cantidad,
                    'Almacenamiento': pedido['zona']
                })
    
    return tabla_pedidos