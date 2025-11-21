"""
Backend Flask - Sistema de Logística FIIS SIE
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from sistema import (
    simular_demanda, procesar_dia_inventario, asignar_picking, planificar_rutas,
    calcular_indicadores, generar_alertas, reporte_logistica,
    dic_sku, dic_clientes, inventario_inicial,
    punto_reposicion, lote_reposicion
)

app = Flask(__name__)
CORS(app)

# Memoria Global
simulacion_actual = {
    'pedidos': {},
    'inventario': inventario_inicial.copy(),
    'indicadores': [],
    'alertas_acumuladas': [],
    'configuracion': {'dias': 7}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simular', methods=['POST'])
def simular():
    global simulacion_actual
    try:
        data = request.get_json()
        n_dias = data.get('dias', 7)
        cap_picking = data.get('capacidad_picking', 1500)
        
        pedidos_simulados = simular_demanda(n_dias, dic_clientes, dic_sku)
        inventario_actual = inventario_inicial.copy() # Inventario al inicio de la simulación
        
        resultados_completos = {}
        indicadores_historia = []
        alertas_totales = []
        
        for dia in range(1, n_dias + 1):
            dia_key = f"Dia_{dia}"
            pedidos_dia = pedidos_simulados.get(dia_key, {})
            
            # 1. Inventario: Calcular flujo (Inicio -> Venta -> Repo -> Final)
            res_inv = procesar_dia_inventario(pedidos_dia, inventario_actual, punto_reposicion, lote_reposicion)
            
            # 2. Picking: IMPORTANTE -> Pasar inventario_actual (del inicio del día)
            res_pick = asignar_picking(dia, pedidos_dia, cap_picking, inventario_actual)
            
            # 3. Transporte
            res_trans = planificar_rutas(dia, res_pick['pedidos_preparados'])
            
            # 4. Indicadores
            total_solicitado = sum(sum(p['productos'].values()) for p in pedidos_dia.values())
            indicadores = calcular_indicadores(
                len(pedidos_dia), res_pick['pedidos_preparados'], res_pick['pedidos_pendientes'],
                res_pick['unidades_preparadas'], total_solicitado, res_trans
            )
            indicadores_historia.append(indicadores)
            
            # 5. Alertas (Acumular)
            alertas_dia = generar_alertas(indicadores)
            for a in alertas_dia:
                a['mensaje'] = f"[Día {dia}] {a['mensaje']}"
            alertas_totales.extend(alertas_dia)
            
            # Guardar resultados
            resultados_completos[dia_key] = {
                'pedidos': pedidos_dia, 'inventario': res_inv, 'picking': res_pick, 
                'transporte': res_trans, 'indicadores': indicadores, 'alertas': alertas_dia
            }
            
            # Actualizar inventario para el día siguiente
            inventario_actual = res_inv['stock_final']

        # Guardar en memoria global
        simulacion_actual['pedidos'] = pedidos_simulados
        simulacion_actual['indicadores'] = indicadores_historia
        simulacion_actual['alertas_acumuladas'] = alertas_totales
        
        return jsonify({'success': True, 'resultados': resultados_completos})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/reporte', methods=['GET'])
def get_reporte():
    if not simulacion_actual['pedidos']: return jsonify({'error': 'No hay datos'}), 404
    # Pasar lista completa de indicadores y alertas
    txt = reporte_logistica(
        simulacion_actual['pedidos'], 
        simulacion_actual['indicadores'], 
        simulacion_actual['alertas_acumuladas']
    )
    return jsonify({'reporte': txt})

@app.route('/api/reset', methods=['POST'])
def reset():
    global simulacion_actual
    simulacion_actual = {'pedidos': {}, 'inventario': inventario_inicial.copy(), 'indicadores': [], 'alertas_acumuladas': []}
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)