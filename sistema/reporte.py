"""
Módulo de Reporte - Sistema de Logística FIIS SIE
Genera reportes consolidados y permite exportación de datos
"""

import datetime
import csv
from .catalogos import dic_clientes, dic_sku

def reporte_logistica(pedidos, indicadores_historia, alertas, periodo="SEMANAL"):
    """
    Genera reporte logístico consolidado con datos acumulados reales.
    """
    resultado = []
    resultado.append("=" * 60)
    resultado.append(f"===== REPORTE LOGÍSTICO {periodo} - LIA S.A.C. =====")
    resultado.append("=" * 60)
    
    # 1. CÁLCULOS REALES (Suma de historiales para evitar ceros)
    total_pedidos = 0
    total_solic = 0
    total_entreg = 0
    
    # Variables para promedios
    sum_otif = 0
    sum_fill = 0
    sum_backlog = 0
    sum_prod = 0
    sum_flota = 0
    n_dias = 0
    
    # Si recibimos una lista (historial completo), sumamos
    if isinstance(indicadores_historia, list):
        n_dias = len(indicadores_historia)
        for ind in indicadores_historia:
            total_pedidos += ind.get('Pedidos_Totales', 0)
            total_solic += ind.get('Unidades_Solicitadas', 0)
            total_entreg += ind.get('Unidades_Entregadas', 0)
            
            sum_otif += ind.get('OTIF', 0)
            sum_fill += ind.get('Fill_Rate', 0)
            sum_backlog += ind.get('Backlog_Rate', 0)
            sum_prod += ind.get('Productividad_Picking', 0)
            sum_flota += ind.get('Utilizacion_Flota', 0)
            
    elif isinstance(indicadores_historia, dict):
        # Caso borde: solo llega un día
        n_dias = 1
        i = indicadores_historia
        total_pedidos = i.get('Pedidos_Totales', 0)
        total_solic = i.get('Unidades_Solicitadas', 0)
        total_entreg = i.get('Unidades_Entregadas', 0)
        
        sum_otif = i.get('OTIF', 0)
        sum_fill = i.get('Fill_Rate', 0)
        sum_backlog = i.get('Backlog_Rate', 0)
        sum_prod = i.get('Productividad_Picking', 0)
        sum_flota = i.get('Utilizacion_Flota', 0)

    # Calcular promedios
    if n_dias > 0:
        otif_global = sum_otif / n_dias
        fill_global = sum_fill / n_dias
        backlog_rate_global = sum_backlog / n_dias
        prod_global = sum_prod / n_dias
        flota_global = sum_flota / n_dias
    else:
        otif_global = fill_global = backlog_rate_global = prod_global = flota_global = 0

    backlog_total = total_solic - total_entreg
    if backlog_total < 0: backlog_total = 0 # Por seguridad

    # 2. IMPRIMIR RESUMEN
    resultado.append(f"\n📊 RESUMEN DE OPERACIONES:")
    resultado.append(f"   • Total pedidos recibidos: {total_pedidos:,}")
    resultado.append(f"   • Total unidades solicitadas: {total_solic:,}")
    resultado.append(f"   • Total unidades entregadas: {total_entreg:,}")
    resultado.append(f"   • Backlog acumulado (unidades): {backlog_total:,}")

    resultado.append(f"\n📈 INDICADORES GLOBALES (Promedio del periodo):")
    resultado.append(f"   • OTIF: {otif_global:.1f}%")
    resultado.append(f"   • Fill Rate: {fill_global:.1f}%")
    resultado.append(f"   • Backlog Rate Promedio: {backlog_rate_global:.1f}%")
    resultado.append(f"   • Productividad de Picking: {prod_global:.1f} unid/h")
    resultado.append(f"   • Utilización de Flota: {flota_global:.1f}%")

    # 3. ALERTAS (Texto completo)
    if alertas:
        resultado.append(f"\n🚨 ALERTAS ACTIVAS (Último corte):")
        for alerta in alertas:
            resultado.append(f"   • {alerta['indicador']}: {alerta['mensaje']}") 
            if 'recomendacion' in alerta:
                resultado.append(f"     -> Acción: {alerta['recomendacion']}")
    else:
        resultado.append(f"\n✅ SIN ALERTAS CRÍTICAS")

    # 4. ANÁLISIS DETALLADO (Top Productos)
    demanda_prod = {}
    demanda_cli = {}
    
    if isinstance(pedidos, dict):
        for dia_data in pedidos.values():
            for p in dia_data.values():
                cli = p['cliente']
                demanda_cli[cli] = demanda_cli.get(cli, 0) + sum(p['productos'].values())
                for sku, cant in p['productos'].items():
                    demanda_prod[sku] = demanda_prod.get(sku, 0) + cant
                    
    resultado.append(f"\n📋 ANÁLISIS DETALLADO:")
    if demanda_cli:
        top_cli = max(demanda_cli, key=demanda_cli.get)
        resultado.append(f"   • Cliente Top: {dic_clientes[top_cli]['nombre']} ({demanda_cli[top_cli]:,} unds)")
    if demanda_prod:
        top_prod = max(demanda_prod, key=demanda_prod.get)
        resultado.append(f"   • Producto Top: {dic_sku[top_prod]['nombre']} ({demanda_prod[top_prod]:,} unds)")

    # 5. RECOMENDACIONES GENERALES
    resultado.append(f"\n💡 RECOMENDACIONES DEL SISTEMA:")
    if otif_global < 95:
        resultado.append("   • Revisar procesos de picking para mejorar tiempos de entrega.")
    if fill_global < 97:
        resultado.append("   • Ajustar puntos de reposición de inventario para evitar quiebres de stock.")
    if flota_global > 90:
        resultado.append("   • Considerar ampliar la flota de transporte por alta saturación.")
    if backlog_rate_global > 5:
        resultado.append("   • Urgente: Aumentar capacidad de picking o turnos extra.")

    resultado.append(f"\n{'='*60}")
    resultado.append(f"Reporte generado el: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    resultado.append("=" * 60)
    
    return "\n".join(resultado)

def exportar_datos_csv(pedidos, indicadores, filename="datos_logistica.csv"):
    """
    Exporta datos para análisis en CSV (Función requerida por __init__)
    """
    datos = []
    
    # Datos de pedidos
    if isinstance(pedidos, dict):
        for dia_key, pedidos_dia in pedidos.items():
            for pedido_id, pedido in pedidos_dia.items():
                for sku, cantidad in pedido['productos'].items():
                    datos.append({
                        'Dia': dia_key,
                        'Pedido_ID': pedido_id,
                        'Cliente': pedido['cliente'],
                        'Zona': pedido['zona'],
                        'SKU': sku,
                        'Cantidad': cantidad
                    })
    
    # Guardar CSV (Opcional, solo si se requiere guardar en disco servidor)
    try:
        if datos:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Dia', 'Pedido_ID', 'Cliente', 'Zona', 'SKU', 'Cantidad']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(datos)
    except Exception:
        pass # Ignorar errores de escritura de archivo en demo
    
    return len(datos)