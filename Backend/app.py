from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "<h1>Hola Mundo x20000 vez</h1>"

@app.route("/ejecutar",methods=['POST'])
def ejecutar():
  codigo = request.json['codigo']
  objeto = {
            'Mensaje': 'Recibido: '+codigo
        }

  return jsonify(objeto)


if __name__ == "__main__":
    app.run(debug=True)