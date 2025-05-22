from flask import Flask, request, jsonify
from minimax import minimax

app = Flask(__name__)

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
    return jsonify({"r": movimiento[0],
    "c": movimiento[1]})


if __name__ == '__main__':
    app.run(debug=True)
