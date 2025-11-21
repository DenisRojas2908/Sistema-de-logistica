"""
Módulo de Reporte - Sistema de Logística FIIS SIE
Formato Ejecutivo (PC3) - Resumen Gerencial
"""
import datetime
from .catalogos import dic_clientes, dic_sku

def reporte_logistica(pedidos, indicadores_historia, alertas_raw, periodo="SEMANAL"):
    resultado = []
    
    # 1. CÁLCULOS DE PROMEDIOS Y TOTALES
    total_pedidos = 0
    total_solic = 0
    total_entreg = 0
    
    sum_otif = 0
    sum_fill = 0
    sum_backlog_rate = 0
    sum_prod = 0
    sum_flota = 0
    
    n_dias = len(indicadores_historia) if isinstance(indicadores_historia, list) else 0
    
    if n_dias > 0:
        for ind in indicadores_historia:
            total_pedidos += ind.get('Pedidos_Totales', 0)
            total_solic += ind.get('Unidades_Solicitadas', 0)
            total_entreg += ind.get('Unidades_Entregadas', 0)
            
            sum_otif += ind.get('OTIF', 0)
            sum_fill += ind.get('Fill_Rate', 0)
            sum_backlog_rate += ind.get('Backlog_Rate', 0)
            sum_prod += ind.get('Productividad_Picking', 0)
            sum_flota += ind.get('Utilizacion_Flota', 0)
            
        # Promedios
        otif_global = sum_otif / n_dias
        fill_global = sum_fill / n_dias
        backlog_rate_global = sum_backlog_rate / n_dias
        prod_global = sum_prod / n_dias
        flota_global = sum_flota / n_dias
    else:
        otif_global = fill_global = backlog_rate_global = prod_global = flota_global = 0

    # Backlog Total en Unidades
    backlog_total_unidades = total_solic - total_entreg
    if backlog_total_unidades < 0: backlog_total_unidades = 0
    
    # Porcentaje de Backlog sobre el total
    porcentaje_backlog_total = (backlog_total_unidades / total_solic * 100) if total_solic > 0 else 0

    # --- GENERACIÓN DEL TEXTO ---

    # CABECERA (MODIFICADA)
    resultado.append(f"===== REPORTE LOGÍSTICO {periodo} - EMPRESA DE LOGÍSTICA =====")
    
    # SECCIÓN 1: Resumen de operaciones
    resultado.append(f"\nResumen de operaciones:")
    resultado.append(f"Total pedidos recibidos: {total_pedidos:,}")
    resultado.append(f"Total unidades solicitadas: {total_solic:,}")
    resultado.append(f"Total unidades entregadas: {total_entreg:,}")
    resultado.append(f"Backlog total: {backlog_total_unidades:,} unidades ({porcentaje_backlog_total:.1f}%)")

    # SECCIÓN 2: Indicadores globales
    resultado.append(f"\nIndicadores globales:")
    resultado.append(f"OTIF: {otif_global:.1f} %")
    resultado.append(f"Fill Rate: {fill_global:.1f} %")
    resultado.append(f"Backlog Rate: {backlog_rate_global:.1f} %")
    resultado.append(f"Productividad de Picking: {prod_global:.2f} unid/h")
    resultado.append(f"Utilización de flota: {flota_global:.1f} %")

    # SECCIÓN 3: Alertas activas (Resumidas)
    resultado.append(f"\nAlertas activas:")
    hay_alertas = False
    
    if otif_global < 95.0:
        resultado.append(f" ⚠️ OTIF bajo ({otif_global:.1f}%)")
        hay_alertas = True
    
    if fill_global < 98.0:
        resultado.append(f" ⚠️ Fill Rate bajo ({fill_global:.1f}%)")
        hay_alertas = True
        
    if flota_global > 85.0:
        resultado.append(f" ⚠️ Utilización alta de flota ({flota_global:.1f}%)")
        hay_alertas = True
        
    if backlog_rate_global > 5.0:
        resultado.append(f" ⚠️ Backlog Rate crítico ({backlog_rate_global:.1f}%)")
        hay_alertas = True

    if not hay_alertas:
        resultado.append(" ✅ Operación estable dentro de los parámetros.")

    # SECCIÓN 4: Recomendaciones
    resultado.append(f"\n ☑️ Recomendaciones:")
    if otif_global < 95.0:
        resultado.append("- Revisar tiempos de preparación y procesos de picking.")
    if fill_global < 98.0:
        resultado.append("- Revisar reaprovisionamiento de inventario y puntos de reorden.")
    if flota_global > 85.0:
        resultado.append("- Incrementar capacidad de flota para evitar saturación.")
    if flota_global < 50.0:
        resultado.append("- Reasignar rutas para optimizar costos de transporte (baja ocupación).")
    if backlog_rate_global > 5.0:
        resultado.append("- Incrementar personal de picking o turnos extra urgentemente.")
    
    if not hay_alertas:
        resultado.append("- Mantener los procesos actuales y monitorear tendencias.")

    resultado.append(f"\n{'-'*50}")
    resultado.append(f"Generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

    return "\n".join(resultado)

def exportar_datos_csv(pedidos, indicadores, filename="datos.csv"):
    return 0