from collections import deque
from models.nodo import nodo
from models.mapa import mapa

Dificultad = 0
ListaNodos = [] # lista de todos los nodos para propagar las utilidades
PosiblesMovimientos = [] # lista de todos los movimientos posibles
MovimientoMax = None # movimiento con la mejor utilidad

#recibe una matriz(mapa del juego) y una dificultad (profundidad maxima)
#devuelve el mejor movimiento para la IA
def minimax(MatrizMapa,dificultad):
    global Dificultad
    global ListaNodos
    global PosiblesMovimientos
    global MovimientoMax

    Dificultad = dificultad
    nodosExpandidos = 0
    NodoInicial = nodo(None, 'max', float('-inf'), mapa(MatrizMapa), 0)
    print("Nodo inicial:  -------------------")
    print(NodoInicial)
    print("-----------------------------------")
    
    pila = deque()
    pila.append(NodoInicial)
    ListaNodos.append(NodoInicial)

    # primero contruimos el arbol completo hasta la profundidad maxima
    while pila:
        nodoActual = pila.pop()
        nodoActual.expandirse(pila)
        nodosExpandidos += 1        
    print("nodos expandidos: ", nodosExpandidos)

    #propagamos las utilidades hacia la raiz y obtenemos el mejor movimiento
    print("Lista nodos totales  ", len(ListaNodos))
    ListaNodos.sort(key=lambda nodo: nodo.profundidad)
    while ListaNodos:
        nodoActual = ListaNodos.pop()
        if nodoActual.padre==None:
            print("Nodo final y su utilidad:  ")
            print(nodoActual)
            print("-----------------------------------")
            break
        if nodoActual.padre.tipo == 'max':
            nodoActual.padre.utilidad = max(nodoActual.padre.utilidad, nodoActual.utilidad)
        else:
            nodoActual.padre.utilidad = min(nodoActual.padre.utilidad, nodoActual.utilidad)
    
    print("numero de posibles movimientos: ")
    print(len(PosiblesMovimientos))
    for movimiento in PosiblesMovimientos:
        if movimiento.utilidad == movimiento.padre.utilidad:
            MovimientoMax = movimiento
    
    return MovimientoMax.mapa.pos_1

