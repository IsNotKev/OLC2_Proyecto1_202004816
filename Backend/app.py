from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

import gramatica as g
import ts as TS
import ejecutar as Ejecutar

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "<h1>Hola Mundo x20000 vez</h1>"

@app.route("/ejecutar",methods=['POST'])
def ejecutar():
  codigo = request.json['codigo']

  instrucciones = g.parse(codigo)
  ts_global = TS.TablaDeSimbolos()
  consola = Ejecutar.procesar_instrucciones(instrucciones, ts_global)

  objeto = {
            'Mensaje': consola
        }

  return jsonify(objeto)


if __name__ == "__main__":
    app.run(debug=True)