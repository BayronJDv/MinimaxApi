# Definición de zonas especiales del mapa
zonaA = [(0,0),(0,1),(0,2),(1,0),(2,0)]
ZonaB = [(0,5),(0,6),(0,7),(1,7),(2,7)]
ZonaC = [(0,5),(0,6),(0,7),(1,7),(2,7)]
ZonaD = [(5,7),(6,7),(7,7),(7,5),(7,6)]

# Lista de todas las zonas
ZONAS = [zonaA, ZonaB, ZonaC, ZonaD]

# Movimientos posibles movimientos de caballo
MOVIMIENTOS = [
    (-2, -1), (-2, +1),
    (-1, -2), (-1, +2),
    (+1, -2), (+1, +2),
    (+2, -1), (+2, +1)
]