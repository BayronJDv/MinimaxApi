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
        if self.profundidad == minimax.Dificultad:
            self.mapa.actualize()
            return
            
        # Verificar si hay un ganador o empate
        resultado = self.mapa.actualize()
        if resultado:
            # Si hay un ganador o empate, actualizar la utilidad y detener la expansión
            if resultado == 'verde':  # IA ganó
                self.utilidad = float('inf') if self.tipo == 'max' else float('-inf')
            elif resultado == 'rojo':  # Jugador ganó
                self.utilidad = float('-inf') if self.tipo == 'max' else float('inf')
            elif resultado == 'empate':
                self.utilidad = 0  # Valor neutral para empate
            return  # Detener la expansión

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

    def calcular_zonas_ganadas(self):
        """
        Devuelve una tupla (ZV, ZR): zonas ganadas por IA (verde) y jugador (rojo)
        """
        ZV = self.mapa.zonasIA
        ZR = self.mapa.zonasJugador
        return ZV, ZR

    def casillas_especiales_no_capturadas(self):
        """
        Devuelve una tupla (CVZ, CVR): casillas especiales pintadas por IA y jugador en zonas NO capturadas aún
        """
        matriz = self.mapa.matriz
        CVZ = 0  # Verde
        CVR = 0  # Rojo
        for zona in ZONAS:
            puntosIA = 0
            puntosJugador = 0
            especiales_IA = []
            especiales_R = []
            for fila, col in zona:
                val = matriz[fila][col]
                if val == 4:
                    puntosIA += 1
                    especiales_IA.append((fila, col))
                elif val == 5:
                    puntosJugador += 1
                    especiales_R.append((fila, col))
                elif val == 1 and self.mapa.es_especial(fila, col):
                    puntosIA += 1
                    especiales_IA.append((fila, col))
                elif val == 2 and self.mapa.es_especial(fila, col):
                    puntosJugador += 1
                    especiales_R.append((fila, col))
            # Solo sumar las casillas especiales de zonas NO capturadas
            if puntosIA < 3:
                CVZ += len(especiales_IA)
            if puntosJugador < 3:
                CVR += len(especiales_R)
        return CVZ, CVR

    # Añadir evaluación del progreso en cada zona
    def evaluar_progreso_zonas(self):
        progreso_IA = 0
        progreso_jugador = 0
        
        for zona in ZONAS:
            puntos_IA = sum(1 for fila, col in zona if 
                        self.mapa.matriz[fila][col] in [1, 4] or 
                        (self.mapa.matriz[fila][col] == 1 and self.mapa.es_especial(fila, col)))
            puntos_jugador = sum(1 for fila, col in zona if 
                            self.mapa.matriz[fila][col] in [2, 5] or 
                            (self.mapa.matriz[fila][col] == 2 and self.mapa.es_especial(fila, col)))
            
            # Bonus por estar cerca de capturar (2/3 casillas especiales)
            if puntos_IA == 2:
                progreso_IA += 50  # Muy cerca de ganar zona
            elif puntos_IA == 1:
                progreso_IA += 20  # Progreso inicial
                
            if puntos_jugador == 2:
                progreso_jugador += 50
            elif puntos_jugador == 1:
                progreso_jugador += 20
        
        return progreso_IA - progreso_jugador

    def calcular_movilidad(self, pos):
        """
        Devuelve el número de movimientos válidos para la posición dada.
        """
        movimientos = 0
        for dx, dy in MOVIMIENTOS:
            nx, ny = pos[0] + dx, pos[1] + dy
            if self.es_movimiento_valido(nx, ny):
                movimientos += 1
        return movimientos


    def evaluar_bloqueo_defensivo(self):
        # Evaluar si se están bloqueando movimientos del oponente
        pos_oponente = self.mapa.pos_2
        
        # Contar cuántos movimientos del oponente llevan a casillas especiales
        movimientos_criticos_bloqueados = 0
        for dx, dy in MOVIMIENTOS:
            nx, ny = pos_oponente[0] + dx, pos_oponente[1] + dy
            if (self.es_movimiento_valido(nx, ny) and 
                self.mapa.es_especial(nx, ny)):
                movimientos_criticos_bloqueados += 1
        
        return movimientos_criticos_bloqueados

    def calcular_utilidad(self):
        ZV, ZR = self.calcular_zonas_ganadas()
        CVZ, CVR = self.casillas_especiales_no_capturadas()
        MVZ = self.calcular_movilidad(self.mapa.pos_1) if self.mapa.pos_1 else 0
        MVR = self.calcular_movilidad(self.mapa.pos_2) if self.mapa.pos_2 else 0
        bloqueo = self.evaluar_bloqueo_defensivo()
        progreso = self.evaluar_progreso_zonas()
        self.utilidad = (1000 * (ZV - ZR) +           
                    100 * progreso +               
                    50 * (CVZ - CVR) +                      
                    10 * bloqueo +                
                    1 * (MVZ - MVR))

    def __str__(self):
        return f"Nodo( tipo :   {self.tipo}, utilidad : {self.utilidad}, profundidad : {self.profundidad},\n mapa : {self.mapa}) "