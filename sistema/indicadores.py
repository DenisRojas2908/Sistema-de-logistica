"""
Módulo de Indicadores - Sistema de Logística FIIS SIE
Cálculo de KPIs de desempeño logístico
"""

def calcular_indicadores(pedidos_recibidos, pedidos_preparados, pedidos_pendientes, 
                        unidades_preparadas, unidades_solicitadas, resultados_transporte):
    """
    Calcula los indicadores clave de desempeño logístico
    
    Args:
        pedidos_recibidos: Total de pedidos recibidos
        pedidos_preparados: Total de pedidos preparados
        pedidos_pendientes: Total de pedidos pendientes
        unidades_preparadas: Total de unidades preparadas
        unidades_solicitadas: Total de unidades solicitadas
        resultados_transporte: Resultados del módulo de transporte
    
    Returns:
        Diccionario con todos los indicadores calculados
    """
    indicadores = {}
    
    # OTIF (On Time In Full) = % de pedidos entregados completos y a tiempo
    # Asumimos que todos los pedidos preparados se entregan a tiempo para simplificar
    pedidos_completados = len(pedidos_preparados)
    indicadores['OTIF'] = (pedidos_completados / pedidos_recibidos * 100) if pedidos_recibidos > 0 else 0
    
    # Fill Rate = unidades entregadas / unidades solicitadas × 100
    indicadores['Fill_Rate'] = (unidades_preparadas / unidades_solicitadas * 100) if unidades_solicitadas > 0 else 0
    
    # Backlog Rate = unidades pendientes / unidades solicitadas × 100
    unidades_pendientes = sum(pedido['total_unidades'] for pedido in pedidos_pendientes.values())
    indicadores['Backlog_Rate'] = (unidades_pendientes / unidades_solicitadas * 100) if unidades_solicitadas > 0 else 0
    
    # Productividad Picking = unidades preparadas / hora (asumiendo 8 horas laborales)
    horas_laborales = 8
    indicadores['Productividad_Picking'] = unidades_preparadas / horas_laborales if unidades_preparadas > 0 else 0
    
    # Utilización de Flota = carga entregada / capacidad disponible × 100
    if resultados_transporte and 'estadisticas' in resultados_transporte:
        indicadores['Utilizacion_Flota'] = resultados_transporte['estadisticas']['utilizacion_promedio']
    else:
        indicadores['Utilizacion_Flota'] = 0
    
    # Indicadores adicionales
    indicadores['Pedidos_Procesados'] = pedidos_completados
    indicadores['Pedidos_Totales'] = pedidos_recibidos
    indicadores['Unidades_Entregadas'] = unidades_preparadas
    indicadores['Unidades_Solicitadas'] = unidades_solicitadas
    indicadores['Unidades_Pendientes'] = unidades_pendientes
    
    return indicadores

def mostrar_indicadores(dia, indicadores):
    """
    Muestra los indicadores de forma formateada
    """
    resultado = [f"\n=== INDICADORES DEL DÍA {dia} ==="]
    resultado.append(f"OTIF: {indicadores['OTIF']:.1f}%")
    resultado.append(f"Fill Rate: {indicadores['Fill_Rate']:.1f}%")
    resultado.append(f"Backlog Rate: {indicadores['Backlog_Rate']:.1f}%")
    resultado.append(f"Productividad de Picking: {indicadores['Productividad_Picking']:.1f} unid/h")
    resultado.append(f"Utilización de Flota: {indicadores['Utilizacion_Flota']:.1f}%")
    
    return "\n".join(resultado)

def calcular_indicadores_acumulados(indicadores_diarios):
    """
    Calcula indicadores acumulados para toda la simulación
    """
    if not indicadores_diarios:
        return {}
    
    # Sumar totales
    total_pedidos = sum(ind['Pedidos_Totales'] for ind in indicadores_diarios)
    total_procesados = sum(ind['Pedidos_Procesados'] for ind in indicadores_diarios)
    total_solicitadas = sum(ind['Unidades_Solicitadas'] for ind in indicadores_diarios)
    total_entregadas = sum(ind['Unidades_Entregadas'] for ind in indicadores_diarios)
    total_pendientes = sum(ind['Unidades_Pendientes'] for ind in indicadores_diarios)
    
    # Calcular promedios ponderados
    otif_acumulado = (total_procesados / total_pedidos * 100) if total_pedidos > 0 else 0
    fill_rate_acumulado = (total_entregadas / total_solicitadas * 100) if total_solicitadas > 0 else 0
    backlog_rate_acumulado = (total_pendientes / total_solicitadas * 100) if total_solicitadas > 0 else 0
    
    # Promedio de utilización de flota
    utilizacion_flota_promedio = sum(ind['Utilizacion_Flota'] for ind in indicadores_diarios) / len(indicadores_diarios)
    
    # Productividad de picking promedio
    productividad_promedio = sum(ind['Productividad_Picking'] for ind in indicadores_diarios) / len(indicadores_diarios)
    
    return {
        'OTIF_Acumulado': otif_acumulado,
        'Fill_Rate_Acumulado': fill_rate_acumulado,
        'Backlog_Rate_Acumulado': backlog_rate_acumulado,
        'Utilizacion_Flota_Promedio': utilizacion_flota_promedio,
        'Productividad_Picking_Promedio': productividad_promedio,
        'Total_Pedidos_Recibidos': total_pedidos,
        'Total_Pedidos_Procesados': total_procesados,
        'Total_Unidades_Solicitadas': total_solicitadas,
        'Total_Unidades_Entregadas': total_entregadas,
        'Total_Unidades_Pendientes': total_pendientes
    }