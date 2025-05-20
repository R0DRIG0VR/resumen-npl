from flask import Flask, request, jsonify
from utils.npl_utils import analizar_texto

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.json
    texto = data.get("texto", "")
    nivel = data.get("resumen_nivel", 30)  # Por defecto 30%

    if not texto:
        return jsonify({"error": "No se envió texto"}), 400

    # Convertir nivel a porcentaje entre 0.1 y 1.0
    porcentaje = max(0.1, min(1.0, nivel / 100))

    resultado = analizar_texto(texto, porcentaje)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
