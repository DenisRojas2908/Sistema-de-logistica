"""
Módulo de Inventario - Sistema de Logística FIIS SIE
Control de inventario y reposición automática
"""

from .catalogos import inventario_inicial, punto_reposicion, lote_reposicion

def reservar_y_actualizar(stock, pedido):
    """
    Reserva stock para un pedido y actualiza el inventario
    
    Args:
        stock: Diccionario con el stock actual
        pedido: Diccionario con los productos del pedido
    
    Returns:
        Tupla (stock_actualizado, pedido_completo, faltantes)
    """
    stock_actualizado = stock.copy()
    pedido_completo = True
    faltantes = {}
    
    for sku, cantidad_solicitada in pedido['productos'].items():
        if sku in stock_actualizado:
            stock_disponible = stock_actualizado[sku]
            
            if stock_disponible >= cantidad_solicitada:
                stock_actualizado[sku] -= cantidad_solicitada
            else:
                # No hay suficiente stock
                pedido_completo = False
                faltantes[sku] = cantidad_solicitada - stock_disponible
                stock_actualizado[sku] = 0  # Se agota el stock
        else:
            # SKU no existe en inventario
            pedido_completo = False
            faltantes[sku] = cantidad_solicitada
    
    return stock_actualizado, pedido_completo, faltantes

def reponer_simple(stock, punto_reorden, lote):
    """
    Genera reposición automática si el stock baja del punto de reorden
    
    Args:
        stock: Diccionario con el stock actual
        punto_reorden: Diccionario con puntos de reorden por SKU
        lote: Diccionario con tamaños de lote por SKU
    
    Returns:
        Tupla (stock_actualizado, reposiciones_realizadas)
    """
    stock_actualizado = stock.copy()
    reposiciones = {}
    
    for sku, stock_actual in stock.items():
        if sku in punto_reorden and stock_actual < punto_reorden[sku]:
            cantidad_reposicion = lote.get(sku, 100)  # Lote por defecto de 100
            stock_actualizado[sku] += cantidad_reposicion
            reposiciones[sku] = cantidad_reposicion
    
    return stock_actualizado, reposiciones

def mostrar_inventario(stock, titulo="Inventario Actual"):
    """
    Muestra el estado del inventario de forma formateada
    """
    resultado = [f"\n=== {titulo} ==="]
    
    for sku, cantidad in stock.items():
        resultado.append(f"{sku}: {cantidad} unidades")
    
    return "\n".join(resultado)

def procesar_dia_inventario(pedidos_dia, stock_inicial, punto_reorden, lote):
    """
    Procesa todos los pedidos de un día y actualiza el inventario
    
    Returns:
        Diccionario con resultados del procesamiento
    """
    stock_actual = stock_inicial.copy()
    pedidos_procesados = []
    total_unidades_despachadas = 0
    
    resultado = ["\n=== Procesamiento de Inventario ==="]
    resultado.append(mostrar_inventario(stock_actual, "Inventario Inicial"))
    
    for pedido_id, pedido in pedidos_dia.items():
        stock_anterior = stock_actual.copy()
        stock_actual, pedido_completo, faltantes = reservar_y_actualizar(stock_actual, pedido)
        
        # Calcular unidades despachadas
        unidades_despachadas = 0
        for sku, cantidad in pedido['productos'].items():
            if sku in stock_anterior:
                despachadas = min(stock_anterior[sku], cantidad)
                unidades_despachadas += despachadas
                if despachadas > 0:
                    resultado.append(f"Pedido {pedido_id} - {sku}: {despachadas} unidades despachadas (Stock restante: {stock_actual[sku]})")
        
        total_unidades_despachadas += unidades_despachadas
        
        pedidos_procesados.append({
            'pedido_id': pedido_id,
            'completo': pedido_completo,
            'faltantes': faltantes,
            'unidades_despachadas': unidades_despachadas
        })
    
    # Verificar reposiciones
    stock_final, reposiciones = reponer_simple(stock_actual, punto_reorden, lote)
    
    if reposiciones:
        resultado.append("\n--- Reaprovisionamiento automático ---")
        for sku, cantidad in reposiciones.items():
            resultado.append(f"{sku}: +{cantidad} unidades añadidas")
    
    resultado.append(mostrar_inventario(stock_final, "Stock Final"))
    
    return {
        'stock_final': stock_final,
        'pedidos_procesados': pedidos_procesados,
        'reposiciones': reposiciones,
        'total_unidades_despachadas': total_unidades_despachadas,
        'log': "\n".join(resultado)
    }