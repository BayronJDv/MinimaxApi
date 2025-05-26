from flask import Flask, request, jsonify
from flask_cors import CORS
from minimax import minimax

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello World"})


@app.route('/api/matriz', methods=['POST'])
def index():
    datos = request.get_json()
    matriz = datos.get('matriz') 
    dificultad = datos.get('dificultad')
    print("calculando...")
    movimiento = minimax(matriz, dificultad)
    print("movimiento calculado")
    print(movimiento)
    # Obtener el estado del ganador usando el mapa resultante
    mapa_resultante = mapa(matriz)
    ganador = mapa_resultante.actualize()

    return jsonify({
        "r": movimiento[0],
        "c": movimiento[1],
        "ganador": ganador
    })



if __name__ == '__main__':
    app.run(debug=True)
