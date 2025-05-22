from flask import Flask, request, jsonify
from minimax import minimax

app = Flask(__name__)

@app.route('/api/matriz', methods=['POST'])
def index():
    datos = request.get_json()
    matriz = datos.get('matriz') 
    dificultad = datos.get('dificultad')
    print("calculando...")
    movimiento = minimax(matriz, dificultad)
    print("movimiento calculado")
    print(movimiento)
    return jsonify({"movimiento": list(movimiento)})

if __name__ == '__main__':
    app.run(debug=True)
