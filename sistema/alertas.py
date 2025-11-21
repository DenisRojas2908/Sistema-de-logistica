"""
Módulo de Alertas - Sistema de Logística FIIS SIE
Genera alertas automáticas basadas en umbrales de indicadores
"""

def generar_alertas(indicadores, umbrales=None):
    """
    Genera alertas automáticas basadas en los indicadores
    
    Args:
        indicadores: Diccionario con indicadores calculados
        umbrales: Diccionario con umbrales para alertas (opcional)
    
    Returns:
        Lista de alertas generadas
    """
    if umbrales is None:
        umbrales = {
            'OTIF_minimo': 95.0,
            'Fill_Rate_minimo': 98.0,
            'Utilizacion_flota_maxima': 85.0,
            'Backlog_rate_maximo': 5.0,
            'Productividad_picking_minima': 150.0
        }
    
    alertas = []
    
    # Alerta por OTIF bajo
    if indicadores['OTIF'] < umbrales['OTIF_minimo']:
        alertas.append({
            'tipo': 'CRÍTICA',
            'indicador': 'OTIF',
            'valor': indicadores['OTIF'],
            'mensaje': f"OTIF menor al {umbrales['OTIF_minimo']}% → Verificar tiempos de preparación y transporte",
            'recomendacion': 'Revisar procesos de picking y coordinación con transporte'
        })
    
    # Alerta por Fill Rate bajo
    if indicadores['Fill_Rate'] < umbrales['Fill_Rate_minimo']:
        alertas.append({
            'tipo': 'IMPORTANTE',
            'indicador': 'Fill Rate',
            'valor': indicadores['Fill_Rate'],
            'mensaje': f"Fill Rate menor al {umbrales['Fill_Rate_minimo']}% → Problemas de disponibilidad de stock",
            'recomendacion': 'Verificar niveles de inventario y punto de reorden'
        })
    
    # Alerta por alta utilización de flota
    if indicadores['Utilizacion_Flota'] > umbrales['Utilizacion_flota_maxima']:
        alertas.append({
            'tipo': 'IMPORTANTE',
            'indicador': 'Utilización Flota',
            'valor': indicadores['Utilizacion_Flota'],
            'mensaje': f"Alta utilización de flota (> {umbrales['Utilizacion_flota_maxima']}%) → Riesgo de saturación",
            'recomendacion': 'Considerar aumentar capacidad de flota o optimizar rutas'
        })
    
    # Alerta por backlog alto
    if indicadores['Backlog_Rate'] > umbrales['Backlog_rate_maximo']:
        alertas.append({
            'tipo': 'IMPORTANTE',
            'indicador': 'Backlog Rate',
            'valor': indicadores['Backlog_Rate'],
            'mensaje': f"Backlog elevado (> {umbrales['Backlog_rate_maximo']}%) → Capacidad insuficiente",
            'recomendacion': 'Incrementar capacidad de picking o revisar planificación'
        })
    
    # Alerta por productividad de picking baja
    if indicadores['Productividad_Picking'] < umbrales['Productividad_picking_minima']:
        alertas.append({
            'tipo': 'INFORMATIVA',
            'indicador': 'Productividad Picking',
            'valor': indicadores['Productividad_Picking'],
            'mensaje': f"Productividad de picking baja (< {umbrales['Productividad_picking_minima']} unid/h)",
            'recomendacion': 'Capacitar personal o revisar layout de almacén'
        })
    
    # Alerta por stock crítico (si hay información de inventario)
    if 'Stock_Critico' in indicadores and indicadores['Stock_Critico']:
        for sku, nivel in indicadores['Stock_Critico'].items():
            alertas.append({
                'tipo': 'CRÍTICA',
                'indicador': 'Stock Crítico',
                'valor': nivel,
                'mensaje': f"Stock crítico para {sku}: {nivel} unidades",
                'recomendacion': 'Solicitar reposición urgente'
            })
    
    return alertas

def mostrar_alertas(alertas):
    """
    Muestra las alertas de forma formateada
    """
    if not alertas:
        return "No hay alertas activas."
    
    resultado = ["\n=== ALERTAS DETECTADAS ==="]
    
    for i, alerta in enumerate(alertas, 1):
        resultado.append(f"\n{i}. Alerta {alerta['tipo']} - {alerta['indicador']}")
        resultado.append(f"   Valor: {alerta['valor']:.1f}")
        resultado.append(f"   Mensaje: {alerta['mensaje']}")
        resultado.append(f"   Recomendación: {alerta['recomendacion']}")
    
    return "\n".join(resultado)

def generar_recomendaciones(alertas):
    """
    Genera recomendaciones automáticas basadas en las alertas
    """
    recomendaciones = []
    
    # Agrupar alertas por tipo
    alertas_criticas = [a for a in alertas if a['tipo'] == 'CRÍTICA']
    alertas_importantes = [a for a in alertas if a['tipo'] == 'IMPORTANTE']
    
    if alertas_criticas:
        recomendaciones.append("🚨 ACCIONES CRÍTICAS INMEDIATAS:")
        for alerta in alertas_criticas:
            recomendaciones.append(f"   • {alerta['recomendacion']}")
    
    if alertas_importantes:
        recomendaciones.append("\n⚠️ ACCIONES IMPORTANTES A CORTO PLAZO:")
        for alerta in alertas_importantes:
            recomendaciones.append(f"   • {alerta['recomendacion']}")
    
    # Recomendaciones generales basadas en patrones
    if len(alertas) >= 3:
        recomendaciones.append("\n📊 RECOMENDACIONES ESTRATÉGICAS:")
        recomendaciones.append("   • Realizar análisis completo de la cadena de suministro")
        recomendaciones.append("   • Considerar implementación de sistema de gestión avanzado")
        recomendaciones.append("   • Revisar contratos con proveedores y clientes")
    
    return recomendaciones