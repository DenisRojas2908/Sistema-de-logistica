"""
Módulo de Inventario - Sistema de Logística FIIS SIE
Control de inventario, ventas y reposición con trazabilidad completa.
"""

def reservar_y_actualizar(stock, pedido):
    """
    Procesa un pedido descontando del stock disponible.
    """
    stock_actualizado = stock.copy()
    pedido_completo = True
    faltantes = {}
    despachado_por_sku = {} # Importante para saber cuánto salió realmente

    # Validación de seguridad por si el pedido viene mal formado
    if 'productos' not in pedido:
        return stock, False, {}, {}

    for sku, cantidad_solicitada in pedido['productos'].items():
        stock_disponible = stock_actualizado.get(sku, 0)
        
        if stock_disponible >= cantidad_solicitada:
            # Hay suficiente stock
            stock_actualizado[sku] -= cantidad_solicitada
            despachado_por_sku[sku] = cantidad_solicitada
        else:
            # Quiebre de stock (Venta parcial)
            pedido_completo = False
            faltantes[sku] = cantidad_solicitada - stock_disponible
            despachado_por_sku[sku] = stock_disponible # Vendemos lo que queda
            stock_actualizado[sku] = 0
            
    return stock_actualizado, pedido_completo, faltantes, despachado_por_sku

def reponer_simple(stock, punto_reorden, lote):
    """
    Verifica si el stock está bajo el mínimo y repone.
    """
    stock_actualizado = stock.copy()
    reposiciones = {}
    
    for sku, cantidad in stock.items():
        # Si el stock actual es menor o igual al punto de reposición
        if sku in punto_reorden and cantidad <= punto_reorden[sku]:
            qty = lote.get(sku, 100)
            stock_actualizado[sku] += qty
            reposiciones[sku] = qty
            
    return stock_actualizado, reposiciones

def procesar_dia_inventario(pedidos_dia, stock_inicial_dia, punto_reorden, lote):
    """
    Orquesta el movimiento diario de inventario:
    1. Foto Inicial -> 2. Ventas -> 3. Reposición -> 4. Foto Final
    """
    # 1. Guardar la foto del inicio del día (Antes de vender)
    stock_al_inicio = stock_inicial_dia.copy()
    
    stock_corriente = stock_inicial_dia.copy()
    ventas_totales_dia = {sku: 0 for sku in stock_inicial_dia}
    
    # 2. Procesar todos los pedidos del día (Descontar stock)
    for pedido in pedidos_dia.values():
        stock_corriente, _, _, despachado = reservar_y_actualizar(stock_corriente, pedido)
        
        # Acumular lo vendido para el reporte
        for sku, cant in despachado.items():
            if sku in ventas_totales_dia:
                ventas_totales_dia[sku] += cant

    # 3. Procesar Reposiciones automáticas (Al final del turno)
    stock_final, reposiciones = reponer_simple(stock_corriente, punto_reorden, lote)
    
    return {
        'stock_inicial': stock_al_inicio,  # Dato clave para tu tabla
        'ventas': ventas_totales_dia,      # Dato clave para saber cuánto salió
        'reposiciones': reposiciones,      # Dato clave para saber cuánto entró
        'stock_final': stock_final         # Dato clave para el día siguiente
    }