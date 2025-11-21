"""
Módulo de Indicadores - Sistema de Logística FIIS SIE
Cálculo de KPIs con protección contra división por cero.
"""

def calcular_indicadores(pedidos_recibidos, pedidos_preparados, pedidos_pendientes, 
                         unidades_preparadas, unidades_solicitadas, resultados_transporte):
    """
    Calcula los 5 KPIs principales.
    """
    indicadores = {}
    
    # 1. OTIF (Pedidos entregados completos)
    pedidos_completados = len(pedidos_preparados)
    if pedidos_recibidos > 0:
        indicadores['OTIF'] = (pedidos_completados / pedidos_recibidos) * 100
    else:
        indicadores['OTIF'] = 100.0 # Si no hay pedidos, técnicamente cumplimos
    
    # 2. Fill Rate (Unidades entregadas vs solicitadas)
    if unidades_solicitadas > 0:
        indicadores['Fill_Rate'] = (unidades_preparadas / unidades_solicitadas) * 100
    else:
        indicadores['Fill_Rate'] = 100.0
    
    # 3. Backlog Rate (Pendientes vs solicitadas)
    if unidades_solicitadas > 0:
        unidades_pendientes = sum(p['total_unidades'] for p in pedidos_pendientes.values())
        indicadores['Backlog_Rate'] = (unidades_pendientes / unidades_solicitadas) * 100
    else:
        indicadores['Backlog_Rate'] = 0.0
        unidades_pendientes = 0
    
    # 4. Productividad Picking (Unidades por hora - Turno 8h)
    horas_laborales = 8
    indicadores['Productividad_Picking'] = unidades_preparadas / horas_laborales
    
    # 5. Utilización de Flota
    # Viene del módulo transporte ya calculado
    if resultados_transporte and 'estadisticas' in resultados_transporte:
        indicadores['Utilizacion_Flota'] = resultados_transporte['estadisticas'].get('utilizacion_promedio', 0)
    else:
        indicadores['Utilizacion_Flota'] = 0
    
    # Guardar valores absolutos para reportes
    indicadores['Pedidos_Procesados'] = pedidos_completados
    indicadores['Pedidos_Totales'] = pedidos_recibidos
    indicadores['Unidades_Entregadas'] = unidades_preparadas
    indicadores['Unidades_Solicitadas'] = unidades_solicitadas
    indicadores['Unidades_Pendientes'] = unidades_pendientes
    
    return indicadores

def mostrar_indicadores(dia, indicadores):
    return "Resumen indicadores generado."

def calcular_indicadores_acumulados(indicadores_diarios):
    return {} # Placeholder para compatibilidad