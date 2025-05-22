import requests


def imprimir_matriz(matriz):
    for fila in matriz:
        print(' '.join(str(elem) for elem in fila))

url = "http://127.0.0.1:5000/api/matriz"
matriz = [[3, 4 ,3, 0, 0, 3, 3, 3], 
          [4, 0, 0, 0, 0, 0, 0, 3],
          [3, 0, 1, 0, 0, 0, 0, 3],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 2, 0, 0, 0, 0],
          [3, 0, 0, 0, 0, 0, 0, 3],
          [3, 0, 0, 0, 0, 0, 0, 5],
          [3, 3, 3, 0, 0, 3, 3, 3],
        ]

response = requests.post(url, json={"matriz": matriz,"dificultad": 2})
movimientor = response.json().get('r')
movimientoc = response.json().get('c')
print(movimientor)
print(movimientoc)