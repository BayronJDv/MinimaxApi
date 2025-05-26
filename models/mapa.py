from constantes import ZONAS

class mapa:
    def __init__(self, matriz):
        self.matriz = matriz
        self.zonasIA = 0
        self.zonasJugador = 0
        self.EspecialesDisponibles = 0
        self.pos_1 = None
        self.pos_2 = None
        self.actualize()
    
    def __str__(self):
        return f"Mapa(\n matriz :\n{self.imprimir_matriz()},\n EspecialesDisponibles : {self.EspecialesDisponibles},\n pos_1 : {self.pos_1},\n pos_2 : {self.pos_2},\n zonasIA : {self.zonasIA},\n zonasJugador : {self.zonasJugador})"

    def actualize(self):
        """Actualiza los atributos derivados de la matriz y retorna el ganador si lo hay"""
        self.EspecialesDisponibles = self.detEspecialesdisponibles()
        self.pos_1, self.pos_2 = self.encontrar_posiciones()
        self.calcular_zonas_tomadas()
        # Lógica para declarar el ganador
        if self.zonasIA >= 3:
            return 'verde'
        elif self.zonasJugador >= 3:
            return 'rojo'
        elif self.zonasIA == 2 and self.zonasJugador == 2:
            return 'empate'
        else:
            return None

    def detEspecialesdisponibles(self):
        disponibles = 0
        for zona in ZONAS:
            for casilla in zona:
                if self.matriz[casilla[0]][casilla[1]] == 3:
                    disponibles += 1
        return disponibles

    def encontrar_posiciones(self):
        pos_1 = None
        pos_2 = None
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if self.matriz[i][j] == 1:
                    pos_1 = (i, j)
                elif self.matriz[i][j] == 2:
                    pos_2 = (i, j)
        return pos_1, pos_2

    def calcular_zonas_tomadas(self):
        self.zonasIA = 0
        self.zonasJugador = 0
        for zona in ZONAS:
            puntosIA = 0
            puntosJugador = 0
            for fila, col in zona:
                valor = self.matriz[fila][col]
                if valor == 4:
                    puntosIA += 1
                elif valor == 5:
                    puntosJugador += 1
                elif valor == 1 and self.es_especial(fila, col):
                    puntosIA += 1
                elif valor == 2 and self.es_especial(fila, col):
                    puntosJugador += 1
            if puntosIA >= 3:
                self.zonasIA += 1
            elif puntosJugador >= 3:
                self.zonasJugador += 1

    #funciones auxiliares
    def imprimir_matriz(self):
        resultado = ""
        for fila in self.matriz:
            resultado += str(fila) + "\n"
        return resultado

    def es_especial(self, i, j):
        for zona in ZONAS:
            if (i, j) in zona:
                return True
        return False
