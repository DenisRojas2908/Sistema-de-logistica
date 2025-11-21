"""
Módulo de Catálogos - Sistema de Logística FIIS SIE
"""

# Catálogo de productos (SKU) - Maquillaje
dic_sku = {
    "P001": {"nombre": "Lápiz Labial", "unidad": "cajas"},
    "P002": {"nombre": "Base", "unidad": "cajas"},
    "P003": {"nombre": "Rubor", "unidad": "cajas"},
    "P004": {"nombre": "Máscara de Pestañas", "unidad": "cajas"},
    "P005": {"nombre": "Sombras de Ojos", "unidad": "cajas"}
}

# Catálogo de clientes (EXPANDIDO: Falabella e Inkafarma en todas las zonas)
dic_clientes = {
    # Clientes exclusivos de zona
    "C01": {"nombre": "AVON", "zona": "Zona Este"},
    "C02": {"nombre": "ESIKA", "zona": "Zona Norte"},
    "C03": {"nombre": "ARUMA", "zona": "Zona Sur"},
    
    # FALABELLA (Presencia Nacional)
    "F01": {"nombre": "FALABELLA", "zona": "Zona Norte"},
    "F02": {"nombre": "FALABELLA", "zona": "Zona Sur"},
    "F03": {"nombre": "FALABELLA", "zona": "Zona Este"},
    "F04": {"nombre": "FALABELLA", "zona": "Zona Oeste"},
    "F05": {"nombre": "FALABELLA", "zona": "Zona Centro"},
    
    # INKAFARMA (Presencia Nacional)
    "I01": {"nombre": "INKAFARMA", "zona": "Zona Norte"},
    "I02": {"nombre": "INKAFARMA", "zona": "Zona Sur"},
    "I03": {"nombre": "INKAFARMA", "zona": "Zona Este"},
    "I04": {"nombre": "INKAFARMA", "zona": "Zona Oeste"},
    "I05": {"nombre": "INKAFARMA", "zona": "Zona Centro"}
}

# Catálogo de vehículos
dic_vehiculos = {
    "V01": {"capacidad": 100, "costo_km": 4.5, "tipo": "Camioneta"},
    "V02": {"capacidad": 120, "costo_km": 5.0, "tipo": "Camión"},
    "V03": {"capacidad": 80, "costo_km": 3.8, "tipo": "Furgoneta"},
    "V04": {"capacidad": 150, "costo_km": 6.2, "tipo": "Camión Grande"},
    "V05": {"capacidad": 90, "costo_km": 4.0, "tipo": "Camioneta"}
}

# Configuración de inventario inicial (Ajustado para ver reposiciones)
inventario_inicial = {
    "P001": 60,
    "P002": 80,
    "P003": 100,
    "P004": 50,
    "P005": 70
}

# Puntos de reposición
punto_reposicion = {
    "P001": 20, "P002": 30, "P003": 35, "P004": 25, "P005": 28
}

# Tamaños de lote
lote_reposicion = {
    "P001": 100, "P002": 150, "P003": 120, "P004": 80, "P005": 90
}