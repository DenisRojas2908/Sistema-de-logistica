from .catalogos import dic_vehiculos, dic_clientes
import random

def planificar_rutas(dia, pedidos_preparados, vehiculos_disponibles=None):
    if vehiculos_disponibles is None:
        vehiculos_disponibles = list(dic_vehiculos.keys())

    pedidos_por_zona = {}
    for pid, pedido in pedidos_preparados.items():
        zona = dic_clientes[pedido['cliente']]['zona']
        if zona not in pedidos_por_zona: pedidos_por_zona[zona] = []
        p_copy = pedido.copy()
        p_copy['id'] = pid
        pedidos_por_zona[zona].append(p_copy)

    rutas_finales = []
    stats = {'total_vehiculos_usados':0, 'total_unidades_transportadas':0, 'utilizacion_promedio':0, 'costo_total':0, 'detalles_rutas':[]}
    suma_util = 0
    count_rutas = 0

    for zona, cola in pedidos_por_zona.items():
        # Mientras haya pedidos en cola para esta zona
        while len(cola) > 0:
            # Elegir vehículo random para variedad
            v_id = random.choice(vehiculos_disponibles)
            cap_max = dic_vehiculos[v_id]['capacidad']
            
            carga_actual = 0
            ids_a_bordo = []
            sobrantes = []

            # Intentar llenar el vehículo
            for pedido in cola:
                peso = pedido['total_unidades']
                if carga_actual + peso <= cap_max:
                    carga_actual += peso
                    ids_a_bordo.append(pedido['id'])
                else:
                    sobrantes.append(pedido) # No cabe, al siguiente camión
            
            # Si logramos cargar algo, registramos la ruta
            if carga_actual > 0:
                util = (carga_actual / cap_max) * 100
                # AJUSTE: Validación de seguridad para nunca pasar 100%
                if util > 100: util = 100 
                
                costo = carga_actual * dic_vehiculos[v_id]['costo_km']
                
                rutas_finales.append({
                    'zona': zona, 'vehiculo': v_id, 'unidades': carga_actual,
                    'capacidad_max': cap_max, 'utilizacion': util, 'costo': costo,
                    'pedidos_ids': ids_a_bordo
                })
                
                stats['total_vehiculos_usados'] += 1
                stats['total_unidades_transportadas'] += carga_actual
                stats['costo_total'] += costo
                suma_util += util
                count_rutas += 1
                
                cola = sobrantes # Continuamos con los que sobraron
            else:
                # Caso borde: El primer pedido es más grande que el camión entero.
                # Lógica: Dividimos el pedido (Split). Llevamos lo que cabe.
                pedido_gigante = cola[0]
                pendiente = pedido_gigante['total_unidades']
                
                while pendiente > 0:
                    # Usar el vehículo actual (o elegir uno grande)
                    llevo = min(pendiente, cap_max)
                    costo_split = llevo * dic_vehiculos[v_id]['costo_km']
                    util_split = (llevo / cap_max) * 100
                    
                    rutas_finales.append({
                        'zona': zona, 'vehiculo': v_id, 'unidades': llevo,
                        'capacidad_max': cap_max, 'utilizacion': util_split, 'costo': costo_split,
                        'pedidos_ids': [pedido_gigante['id'] + " (Parcial)"]
                    })
                    
                    stats['total_vehiculos_usados'] += 1
                    stats['costo_total'] += costo_split
                    suma_util += util_split
                    count_rutas += 1
                    
                    pendiente -= llevo
                    # Para el siguiente trozo, elegimos otro vehiculo (loop) o el mismo
                    if pendiente > 0:
                        v_id = random.choice(vehiculos_disponibles)
                        cap_max = dic_vehiculos[v_id]['capacidad']
                
                # Quitamos el pedido gigante de la cola ya procesada
                cola.pop(0)
                # Y agregamos los demás sobrantes si había
                cola.extend(sobrantes)
                sobrantes = []

    stats['detalles_rutas'] = rutas_finales
    if count_rutas > 0: stats['utilizacion_promedio'] = suma_util / count_rutas
    
    return {'rutas': rutas_finales, 'estadisticas': stats}

def mostrar_transporte_dia(d, r): return ""
def generar_programa_transporte(d, p): return {}