from constantes import MOVIMIENTOS, ZONAS
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
        if self.profundidad == minimax.Dificultad or self.termino_el_juego():
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
                if nuevoNodo.profundidad == minimax.Dificultad or nuevoNodo.termino_el_juego():
                    nuevoNodo.calcular_utilidad()


                #si es hijo del nodo raiz (profundidad 0) lo agregamos a la lista de posibles movimientos
                if self.profundidad == 0 :
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
        ZV = self.mapa.zonasIA  # Zonas ganadas por la IA (verde)
        ZR = self.mapa.zonasJugador  # Zonas ganadas por el rival (rojo)

        # Condición de victoria o derrota inmediata
        if ZV >= 3:
            self.utilidad = float('inf')
            return
        elif ZR >= 3:
            self.utilidad = float('-inf')
            return

        matriz = self.mapa.matriz
        CVZ = 0  # Casillas especiales pintadas por IA en zonas no capturadas
        CVR = 0  # Casillas especiales pintadas por rival en zonas no capturadas
        zonas_casi_ganadas_ia = 0
        zonas_casi_ganadas_rival = 0

        for zona in ZONAS:
            puntosIA = 0
            puntosJugador = 0
            for fila, col in zona:
                val = matriz[fila][col]
                if val == 4 or (val == 1 and self.mapa.es_especial(fila, col)):
                    puntosIA += 1
                elif val == 5 or (val == 2 and self.mapa.es_especial(fila, col)):
                    puntosJugador += 1
            if puntosIA < 3:
                CVZ += puntosIA
            if puntosJugador < 3:
                CVR += puntosJugador
            # Detecta zonas casi ganadas
            if puntosIA == 2 and puntosJugador < 2:
                zonas_casi_ganadas_ia += 1
            if puntosJugador == 2 and puntosIA < 2:
                zonas_casi_ganadas_rival += 1

        # Movilidad (número de movimientos válidos)
        def contar_movilidad(pos):
            movimientos = 0
            for dx, dy in MOVIMIENTOS:
                nx, ny = pos[0] + dx, pos[1] + dy
                if self.es_movimiento_valido(nx, ny):
                    movimientos += 1
            return movimientos

        MVZ = contar_movilidad(self.mapa.pos_1) if self.mapa.pos_1 else 0
        MVR = contar_movilidad(self.mapa.pos_2) if self.mapa.pos_2 else 0

        # Ajuste de pesos según etapa del juego
        zonas_capturadas = ZV + ZR
        if zonas_capturadas == 0:
            # Etapa temprana: priorizar zonas casi ganadas
            w_zonas = 100
            w_casi = 30
            w_casillas = 10
            w_mov = 3
        elif zonas_capturadas < 3:
            # Etapa media: balance entre capturar zonas y asegurar casillas
            w_zonas = 100
            w_casi = 5
            w_casillas = 20
            w_mov = 2
        else:
            # Etapa final: asegurar la última zona
            w_zonas = 100
            w_casi = 0
            w_casillas = 30
            w_mov = 1

        self.utilidad = (
            w_zonas * (ZV - ZR) +
            w_casi * (zonas_casi_ganadas_ia - zonas_casi_ganadas_rival) +
            w_casillas * (CVZ - CVR) +
            w_mov * (MVZ - MVR)
        )


    def termino_el_juego(self):
        if self.mapa.zonasIA + self.mapa.zonasJugador == 4:
            return True
        return False

    def __str__(self):
        return f"Nodo( tipo :   {self.tipo}, utilidad : {self.utilidad}, profundidad : {self.profundidad},\n mapa : {self.mapa}) "