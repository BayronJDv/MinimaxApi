from constantes import MOVIMIENTOS
import minimax
import copy


class nodo:
    def __init__(self, padre, tipo, utilidad, mapa, profundidad):
        #estado actual del mapa
        self.mapa = mapa

        self.tipo = tipo
        self.padre = padre
        self.utilidad = float('-inf') if self.tipo == 'max' else float('inf')
        self.profundidad = profundidad;

    def expandirse(self, pila):
        #si se alcanza la profundidad maxima, calcular utilidad
        if self.profundidad == minimax.Dificultad:
            self.mapa.actualize()
            return

        x = self.mapa.pos_1[0] if self.tipo == 'max' else self.mapa.pos_2[0]
        y = self.mapa.pos_1[1] if self.tipo == 'max' else self.mapa.pos_2[1]            

        for movimiento in MOVIMIENTOS:
            nx = x + movimiento[0]
            ny = y + movimiento[1]
            if self.es_movimiento_valido(nx, ny): 
                nuevoMapa = copy.deepcopy(self.mapa)

                # Si se mueve desde una casilla especial, marcarla como tomada
                if nuevoMapa.es_especial(x, y):
                    nuevoMapa.matriz[x][y] = 4 if self.tipo == 'max' else 5
                else:
                    nuevoMapa.matriz[x][y] = 0

                # Colocar al jugador en la nueva casilla
                nuevoMapa.matriz[nx][ny] = 1 if self.tipo == 'max' else 2 

                nuevotipo = 'min' if self.tipo == 'max' else 'max'
                nuevaProfundidad = self.profundidad + 1
                nuevoMapa.actualize()
                nuevoNodo = nodo(self, nuevotipo, 0, nuevoMapa, nuevaProfundidad)
                if nuevoNodo.profundidad == minimax.Dificultad:
                    nuevoNodo.calcular_utilidad()
                #print("nuevo nodo :\n")
                #print(nuevoNodo)

                #si es hijo del nodo raiz (profundidad 0) lo agregamos a la lista de posibles movimientos
                if self.profundidad == 0:
                    minimax.PosiblesMovimientos.append(nuevoNodo)
                    
                #agregamos el nuevo nodo a la lista de nodos y a la pila
                minimax.ListaNodos.append(nuevoNodo)
                pila.append(nuevoNodo)              
        
    def es_movimiento_valido(self, fila_destino, col_destino):        
        # Verificar que las coordenadas estén dentro del tablero
        filas = len(self.mapa.matriz)
        columnas = len(self.mapa.matriz[0]) if filas > 0 else 0
        
        if (fila_destino < 0 or fila_destino >= filas or 
            col_destino < 0 or col_destino >= columnas):
            return False
        
        valor_destino = self.mapa.matriz[fila_destino][col_destino]
        
        if valor_destino == 0 or valor_destino == 3:
            return True
        
        return False

    def calcular_utilidad(self):
        self.utilidad = self.mapa.zonasIA - self.mapa.zonasJugador

    def __str__(self):
        return f"Nodo( tipo :   {self.tipo}, utilidad : {self.utilidad}, profundidad : {self.profundidad},\n mapa : {self.mapa}) "