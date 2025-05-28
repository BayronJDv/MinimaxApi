from flask import Flask, request, jsonify
from flask_cors import CORS
from minimax import minimax
from models.mapa import mapa
import os

app = Flask(__name__)

frontend_origin = os.environ.get("FRONTEND_ORIGIN")

if frontend_origin:
    CORS(app, resources={r"/*": {"origins": frontend_origin}})
else:
    CORS(app)

@app.route("/")
def home():
    return "¡API Flask con CORS usando variables de entorno!"

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
    print("ganador: ", ganador)

    return jsonify({
        "r": movimiento[0],
        "c": movimiento[1],
        "ganador": ganador
    })



if __name__ == '__main__':
    app.run(debug=True)
