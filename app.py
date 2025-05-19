from flask import Flask, request, jsonify
from utils.npl_utils import analizar_texto

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    texto = request.json.get("texto", "")
    if not texto:
        return jsonify({"error": "No se envió texto"}), 400
    resultado = analizar_texto(texto)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
