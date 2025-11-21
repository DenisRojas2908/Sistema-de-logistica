"""
Backend Flask - Sistema de Logística FIIS SIE
API REST para el sistema de simulación logística
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os
from sistema import (
    simular_demanda, mostrar_simulacion, exportar_pedidos_tabla,
    procesar_dia_inventario, asignar_picking, planificar_rutas,
    calcular_indicadores, generar_alertas, reporte_logistica,
    dic_sku, dic_clientes, dic_vehiculos, inventario_inicial,
    punto_reposicion, lote_reposicion
)

app = Flask(__name__)
CORS(app)

# Variables globales para almacenar el estado de la simulación
simulacion_actual = {
    'pedidos': {},
    'inventario': inventario_inicial.copy(),
    'indicadores': {},
    'alertas': [],
    'configuracion': {
        'dias_simulacion': 7,
        'capacidad_picking': 1500,
        'mostrar_detalles': False
    }
}

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/catalogos', methods=['GET'])
def get_catalogos():
    """Obtener catálogos de productos, clientes y vehículos"""
    return jsonify({
        'productos': dic_sku,
        'clientes': dic_clientes,
        'vehiculos': dic_vehiculos,
        'inventario_inicial': inventario_inicial,
        'puntos_reposicion': punto_reposicion
    })

@app.route('/api/simular', methods=['POST'])
def simular():
    """Ejecutar simulación logística"""
    global simulacion_actual
    
    try:
        data = request.get_json()
        n_dias = data.get('dias', 7)
        capacidad_picking = data.get('capacidad_picking', 1500)
        
        # Simular demanda
        pedidos_simulados = simular_demanda(n_dias, dic_clientes, dic_sku)
        
        # Procesar cada día
        resultados_completos = {}
        indicadores_diarios = []
        inventario_actual = inventario_inicial.copy()
        
        for dia in range(1, n_dias + 1):
            dia_key = f"Dia_{dia}"
            
            if dia_key in pedidos_simulados:
                pedidos_dia = pedidos_simulados[dia_key]
                
                # Procesar inventario
                resultado_inventario = procesar_dia_inventario(
                    pedidos_dia, inventario_actual, punto_reposicion, lote_reposicion
                )
                inventario_actual = resultado_inventario['stock_final']
                
                # Procesar picking
                resultados_picking = asignar_picking(dia, pedidos_dia, capacidad_picking)
                
                # Planificar transporte
                resultados_transporte = planificar_rutas(dia, resultados_picking['pedidos_preparados'])
                
                # Calcular indicadores
                indicadores = calcular_indicadores(
                    len(pedidos_dia),
                    resultados_picking['pedidos_preparados'],
                    resultados_picking['pedidos_pendientes'],
                    resultados_picking['unidades_preparadas'],
                    resultados_picking['unidades_preparadas'] + resultados_picking['backlog'],
                    resultados_transporte
                )
                
                # Generar alertas
                alertas = generar_alertas(indicadores)
                
                # Guardar resultados del día
                resultados_completos[dia_key] = {
                    'pedidos': pedidos_dia,
                    'inventario': resultado_inventario,
                    'picking': resultados_picking,
                    'transporte': resultados_transporte,
                    'indicadores': indicadores,
                    'alertas': alertas
                }
                
                indicadores_diarios.append(indicadores)
        
        # Actualizar simulación actual
        simulacion_actual['pedidos'] = pedidos_simulados
        simulacion_actual['inventario'] = inventario_actual
        simulacion_actual['indicadores'] = indicadores_diarios
        simulacion_actual['alertas'] = alertas
        
        return jsonify({
            'success': True,
            'resultados': resultados_completos,
            'resumen': {
                'dias_simulados': n_dias,
                'total_pedidos': sum(len(pedidos_dia) for pedidos_dia in pedidos_simulados.values()),
                'indicadores_finales': indicadores_diarios[-1] if indicadores_diarios else {}
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/indicadores', methods=['GET'])
def get_indicadores():
    """Obtener indicadores de la simulación actual"""
    if not simulacion_actual['indicadores']:
        return jsonify({
            'error': 'No hay simulación activa'
        }), 404
    
    return jsonify({
        'indicadores': simulacion_actual['indicadores'],
        'alertas': simulacion_actual['alertas']
    })

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    """Obtener pedidos de la simulación actual"""
    if not simulacion_actual['pedidos']:
        return jsonify({
            'error': 'No hay simulación activa'
        }), 404
    
    # Exportar en formato tabla
    tabla_pedidos = exportar_pedidos_tabla(simulacion_actual['pedidos'])
    
    return jsonify({
        'pedidos_tabla': tabla_pedidos,
        'pedidos_estructurados': simulacion_actual['pedidos']
    })

@app.route('/api/reporte', methods=['GET'])
def get_reporte():
    """Generar reporte completo"""
    if not simulacion_actual['pedidos']:
        return jsonify({'error': 'No hay simulación activa'}), 404
    
    # CORRECCIÓN: Pasamos TODA la lista de indicadores, no solo el último
    lista_indicadores = simulacion_actual['indicadores']
    alertas_finales = simulacion_actual['alertas']
    
    reporte_texto = reporte_logistica(
        simulacion_actual['pedidos'],
        lista_indicadores, # <--- AQUÍ ESTABA EL ERROR (Antes pasaba solo un dict)
        alertas_finales
    )
    
    return jsonify({
        'reporte': reporte_texto
    })

@app.route('/api/configuracion', methods=['GET', 'POST'])
def configuracion():
    """Obtener o actualizar configuración"""
    global simulacion_actual
    
    if request.method == 'GET':
        return jsonify(simulacion_actual['configuracion'])
    
    elif request.method == 'POST':
        data = request.get_json()
        simulacion_actual['configuracion'].update(data)
        return jsonify({
            'success': True,
            'configuracion': simulacion_actual['configuracion']
        })

@app.route('/api/reset', methods=['POST'])
def reset():
    """Resetear la simulación"""
    global simulacion_actual
    
    simulacion_actual = {
        'pedidos': {},
        'inventario': inventario_inicial.copy(),
        'indicadores': {},
        'alertas': [],
        'configuracion': {
            'dias_simulacion': 7,
            'capacidad_picking': 1500,
            'mostrar_detalles': False
        }
    }
    
    return jsonify({
        'success': True,
        'message': 'Simulación reiniciada'
    })

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, host='0.0.0.0', port=5000)