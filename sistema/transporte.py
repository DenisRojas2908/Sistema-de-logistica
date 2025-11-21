"""
Módulo de Transporte - Sistema de Logística FIIS SIE
Planificación de rutas y asignación de vehículos (Corregido)
"""

from .catalogos import dic_vehiculos, dic_clientes
import random

def planificar_rutas(dia, pedidos_preparados, vehiculos_disponibles=None):
    if vehiculos_disponibles is None:
        vehiculos_disponibles = list(dic_vehiculos.keys())

    # 1. Agrupar pedidos por zona
    pedidos_por_zona = {}
    for pedido_id, pedido in pedidos_preparados.items():
        zona = dic_clientes[pedido['cliente']]['zona']
        if zona not in pedidos_por_zona:
            pedidos_por_zona[zona] = []
        
        pedido_con_id = pedido.copy()
        pedido_con_id['id'] = pedido_id
        pedidos_por_zona[zona].append(pedido_con_id)

    rutas_finales = []
    estadisticas = {
        'total_vehiculos_usados': 0,
        'total_unidades_transportadas': 0,
        'utilizacion_promedio': 0,
        'costo_total': 0,
        'detalles_rutas': [] 
    }

    suma_utilizacion = 0
    count_rutas = 0

    # 2. Procesar cada zona
    for zona, cola_pedidos in pedidos_por_zona.items():
        
        # Mientras queden pedidos en la zona...
        while len(cola_pedidos) > 0:
            # Elegir vehículo aleatorio para variedad
            vehiculo_id = random.choice(vehiculos_disponibles)
            capacidad_max = dic_vehiculos[vehiculo_id]['capacidad']
            
            carga_actual = 0
            ids_en_camion = []
            pedidos_no_entraron = []

            # Llenar el camión pedido por pedido
            for pedido in cola_pedidos:
                peso_pedido = pedido['total_unidades']
                
                # Si el pedido cabe, lo subimos
                if carga_actual + peso_pedido <= capacidad_max:
                    carga_actual += peso_pedido
                    ids_en_camion.append(pedido['id'])
                else:
                    # Si no cabe, se queda para el siguiente camión
                    pedidos_no_entraron.append(pedido)
            
            # Registrar la ruta si cargamos algo
            if carga_actual > 0:
                utilizacion = (carga_actual / capacidad_max) * 100
                costo = carga_actual * dic_vehiculos[vehiculo_id]['costo_km']
                
                rutas_finales.append({
                    'zona': zona,
                    'vehiculo': vehiculo_id,
                    'unidades': carga_actual,
                    'capacidad_max': capacidad_max,
                    'utilizacion': utilizacion,
                    'costo': costo,
                    'pedidos_ids': ids_en_camion
                })
                
                estadisticas['total_vehiculos_usados'] += 1
                estadisticas['total_unidades_transportadas'] += carga_actual
                estadisticas['costo_total'] += costo
                suma_utilizacion += utilizacion
                count_rutas += 1
                
                cola_pedidos = pedidos_no_entraron
            else:
                # Caso borde: El primer pedido es más grande que el camión entero
                # Forzamos split simple para no romper el loop
                top_pedido = cola_pedidos.pop(0)
                rutas_finales.append({
                    'zona': zona, 'vehiculo': vehiculo_id, 
                    'unidades': capacidad_max, 'capacidad_max': capacidad_max, 
                    'utilizacion': 100.0, 'costo': capacidad_max * 5.0,
                    'pedidos_ids': [top_pedido['id'] + " (Split)"]
                })
                count_rutas += 1
                suma_utilizacion += 100

    estadisticas['detalles_rutas'] = rutas_finales
    if count_rutas > 0:
        estadisticas['utilizacion_promedio'] = suma_utilizacion / count_rutas

    return {
        'rutas': rutas_finales,
        'estadisticas': estadisticas
    }

def mostrar_transporte_dia(d,r): return ""
def generar_programa_transporte(d,p): return {}