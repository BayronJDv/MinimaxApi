# API Minimax para Juego de Tablero

## Descripción

Este proyecto implementa una API que utiliza el algoritmo Minimax para calcular movimientos óptimos en un juego de tablero. La API recibe el estado actual del tablero y devuelve el mejor movimiento posible para la IA.

## Características

- Implementación del algoritmo Minimax para la toma de decisiones
- API REST construida con Flask
- Movimientos tipo caballo de ajedrez
- Sistema de zonas especiales que pueden ser capturadas
- Diferentes niveles de dificultad (profundidad del algoritmo Minimax)

## Cómo funciona

1. El cliente envía una petición POST a `/api/matriz` con:
   - Una matriz que representa el estado actual del tablero
   - Un nivel de dificultad

2. El servidor procesa la petición utilizando el algoritmo Minimax para calcular el mejor movimiento

3. El servidor devuelve las coordenadas del movimiento óptimo en formato JSON

## Representación del tablero

El tablero se representa como una matriz donde:
- `0`: Casilla vacía
- `1`: Posición del jugador IA
- `2`: Posición del jugador humano
- `3`: Casilla especial disponible
- `4`: Casilla especial capturada por la IA
- `5`: Casilla especial capturada por el jugador humano

## Ejemplo de uso

Puedes encontrar un ejemplo de cómo utilizar la API en el archivo `req.py`, que muestra cómo enviar una petición al servidor y procesar la respuesta.