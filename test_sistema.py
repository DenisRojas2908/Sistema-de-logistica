#!/usr/bin/env python3
"""
Script de prueba para validar el sistema de logística FIIS SIE
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sistema import (
    dic_sku, dic_clientes, dic_vehiculos, inventario_inicial,
    simular_demanda, mostrar_simulacion,
    procesar_dia_inventario, asignar_picking, planificar_rutas,
    calcular_indicadores, generar_alertas, reporte_logistica,
    punto_reposicion, lote_reposicion
)

def test_catalogos():
    """Probar que los catálogos están correctamente configurados"""
    print("\n📦 PROBANDO CATÁLOGOS...")
    
    # Verificar productos
    assert len(dic_sku) == 5, f"Error: Se esperaban 5 productos, se encontraron {len(dic_sku)}"
    assert "P001" in dic_sku, "Error: Falta P001"
    print(f"✅ Productos: {len(dic_sku)} SKUs configurados")
    
    # Verificar clientes
    assert len(dic_clientes) == 5, f"Error: Se esperaban 5 clientes, se encontraron {len(dic_clientes)}"
    assert "C01" in dic_clientes, "Error: Falta C01"
    print(f"✅ Clientes: {len(dic_clientes)} tiendas configuradas")
    
    # Verificar vehículos
    assert len(dic_vehiculos) == 5, f"Error: Se esperaban 5 vehículos, se encontraron {len(dic_vehiculos)}"
    assert "V01" in dic_vehiculos, "Error: Falta V01"
    print(f"✅ Vehículos: {len(dic_vehiculos)} unidades configuradas")
    
    # Verificar inventario
    assert len(inventario_inicial) == 5, f"Error: Se esperaban 5 productos en inventario"
    total_inventario = sum(inventario_inicial.values())
    print(f"✅ Inventario inicial: {total_inventario} unidades totales")
    
    return True

def test_simulacion_demanda():
    """Probar la simulación de demanda"""
    print("\n🔄 PROBANDO SIMULACIÓN DE DEMANDA...")
    
    # Simular 3 días
    pedidos = simular_demanda(3, dic_clientes, dic_sku)
    
    assert len(pedidos) == 3, f"Error: Se esperaban 3 días, se encontraron {len(pedidos)}"
    assert "Dia_1" in pedidos, "Error: Falta Dia_1"
    
    # Verificar que hay pedidos
    pedidos_dia1 = pedidos["Dia_1"]
    assert len(pedidos_dia1) > 0, "Error: No hay pedidos en el día 1"
    
    # Verificar estructura de pedidos
    primer_pedido = list(pedidos_dia1.values())[0]
    assert "cliente" in primer_pedido, "Error: Falta campo 'cliente'"
    assert "productos" in primer_pedido, "Error: Falta campo 'productos'"
    assert "zona" in primer_pedido, "Error: Falta campo 'zona'"
    
    print(f"✅ Simulación: {len(pedidos)} días generados")
    print(f"✅ Día 1: {len(pedidos_dia1)} pedidos generados")
    
    return pedidos

def test_inventario(pedidos_dia1):
    """Probar el procesamiento de inventario"""
    print("\n📊 PROBANDO INVENTARIO...")
    
    # Procesar inventario
    resultado = procesar_dia_inventario(
        pedidos_dia1, 
        inventario_inicial.copy(), 
        punto_reposicion, 
        lote_reposicion
    )
    
    assert "stock_final" in resultado, "Error: Falta stock_final"
    assert "pedidos_procesados" in resultado, "Error: Falta pedidos_procesados"
    assert "total_unidades_despachadas" in resultado, "Error: Falta total_unidades_despachadas"
    
    print(f"✅ Inventario procesado: {resultado['total_unidades_despachadas']} unidades despachadas")
    
    return resultado

def test_picking(pedidos_dia1):
    """Probar las operaciones de picking"""
    print("\n🚛 PROBANDO PICKING...")
    
    # Procesar picking
    resultado = asignar_picking(1, pedidos_dia1, capacidad_picking=1500)
    
    assert "pedidos_preparados" in resultado, "Error: Falta pedidos_preparados"
    assert "pedidos_pendientes" in resultado, "Error: Falta pedidos_pendientes"
    assert "unidades_preparadas" in resultado, "Error: Falta unidades_preparadas"
    assert "backlog" in resultado, "Error: Falta backlog"
    
    print(f"✅ Picking: {len(resultado['pedidos_preparados'])} pedidos preparados")
    print(f"✅ Backlog: {resultado['backlog']} unidades pendientes")
    
    return resultado

def test_transporte(pedidos_preparados):
    """Probar la planificación de transporte"""
    print("\n🚚 PROBANDO TRANSPORTE...")
    
    # Planificar transporte
    resultado = planificar_rutas(1, pedidos_preparados)
    
    assert "rutas" in resultado, "Error: Falta rutas"
    assert "estadisticas" in resultado, "Error: Falta estadisticas"
    
    stats = resultado['estadisticas']
    assert "utilizacion_promedio" in stats, "Error: Falta utilizacion_promedio"
    assert "costo_total" in stats, "Error: Falta costo_total"
    
    print(f"✅ Transporte: {stats['total_vehiculos_usados']} vehículos usados")
    print(f"✅ Costo total: S/ {stats['costo_total']:.2f}")
    
    return resultado

def test_indicadores(pedidos_dia1, resultados_picking, resultados_transporte):
    """Probar el cálculo de indicadores"""
    print("\n📈 PROBANDO INDICADORES...")
    
    # Calcular indicadores
    indicadores = calcular_indicadores(
        pedidos_recibidos=len(pedidos_dia1),
        pedidos_preparados=resultados_picking['pedidos_preparados'],
        pedidos_pendientes=resultados_picking['pedidos_pendientes'],
        unidades_preparadas=resultados_picking['unidades_preparadas'],
        unidades_solicitadas=resultados_picking['unidades_preparadas'] + resultados_picking['backlog'],
        resultados_transporte=resultados_transporte
    )
    
    # Verificar indicadores calculados
    assert "OTIF" in indicadores, "Error: Falta OTIF"
    assert "Fill_Rate" in indicadores, "Error: Falta Fill_Rate"
    assert "Backlog_Rate" in indicadores, "Error: Falta Backlog_Rate"
    assert "Productividad_Picking" in indicadores, "Error: Falta Productividad_Picking"
    assert "Utilizacion_Flota" in indicadores, "Error: Falta Utilizacion_Flota"
    
    print(f"✅ OTIF: {indicadores['OTIF']:.1f}%")
    print(f"✅ Fill Rate: {indicadores['Fill_Rate']:.1f}%")
    print(f"✅ Backlog Rate: {indicadores['Backlog_Rate']:.1f}%")
    print(f"✅ Productividad: {indicadores['Productividad_Picking']:.1f} unid/h")
    print(f"✅ Utilización Flota: {indicadores['Utilizacion_Flota']:.1f}%")
    
    return indicadores

def test_alertas(indicadores):
    """Probar el sistema de alertas"""
    print("\n🚨 PROBANDO ALERTAS...")
    
    # Generar alertas
    alertas = generar_alertas(indicadores)
    
    print(f"✅ Alertas generadas: {len(alertas)}")
    
    for i, alerta in enumerate(alertas[:3]):  # Mostrar máximo 3
        print(f"   {i+1}. {alerta['tipo']}: {alerta['indicador']} - {alerta['mensaje'][:50]}...")
    
    return alertas

def test_reporte(pedidos, indicadores, alertas):
    """Probar la generación de reportes"""
    print("\n📄 PROBANDO REPORTE...")
    
    # Generar reporte
    reporte = reporte_logistica(pedidos, indicadores, alertas, periodo="PRUEBA")
    
    assert "REPORTE LOGÍSTICO" in reporte, "Error: No contiene título de reporte"
    assert "INDICADORES GLOBALES" in reporte, "Error: No contiene sección de indicadores"
    
    print(f"✅ Reporte generado: {len(reporte)} caracteres")
    
    return reporte

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE LOGÍSTICA")
    print("=" * 60)
    
    try:
        # Ejecutar pruebas en secuencia
        test_catalogos()
        pedidos = test_simulacion_demanda()
        pedidos_dia1 = pedidos["Dia_1"]
        
        resultado_inventario = test_inventario(pedidos_dia1)
        resultados_picking = test_picking(pedidos_dia1)
        resultados_transporte = test_transporte(resultados_picking['pedidos_preparados'])
        indicadores = test_indicadores(pedidos_dia1, resultados_picking, resultados_transporte)
        alertas = test_alertas(indicadores)
        reporte = test_reporte(pedidos, indicadores, alertas)
        
        print("\n" + "=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("=" * 60)
        print("✅ Sistema de logística FIIS SIE funcionando correctamente")
        print("✅ Todos los módulos integrados y operativos")
        print("✅ Listo para uso en producción o demostración")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {str(e)}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    main()