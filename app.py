from flask import Flask, request, jsonify
from utils.npl_utils import analizar_texto
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from PyPDF2 import PdfReader

app = Flask(__name__)

# ----------------------------------------
# STOPWORDS SIMPLES PARA DETECCIÓN IDIOMA
# ----------------------------------------
spanish_stopwords = {
    "el", "la", "y", "de", "que", "en", "a", "los", "se", "del",
    "las", "por", "un", "para", "con", "no", "una", "su", "al", "lo"
}


def detectar_idioma_simple(texto: str) -> str:
    """
    Método muy básico para detectar si el texto está mayoritariamente en español o inglés.
    Se cuenta cuántas stopwords en inglés vs español aparecen, y se elige el idioma con más coincidencias.
    Si hay empate o muy pocas coincidencias, devuelve 'unknown'.
    """
    tokens = re.findall(r"\b\w+\b", texto.lower())
    count_en = sum(1 for t in tokens if t in ENGLISH_STOP_WORDS)
    count_es = sum(1 for t in tokens if t in spanish_stopwords)

    if count_en > count_es and count_en >= 3:
        return "en"
    if count_es > count_en and count_es >= 3:
        return "es"
    return "unknown"


@app.route("/analizar", methods=["POST"])
def analizar():
    """
    Endpoint JSON para resumir texto plano.
    Body JSON esperado:
      {
        "texto": "…",
        "resumen_nivel": 30,    # porcentaje (0–100)
        "lang": "es"           # "es" o "en" (por defecto "es")
      }
    """
    data = request.get_json(force=True) or {}
    texto = data.get("texto", "")
    if not isinstance(texto, str) or texto.strip() == "":
        return jsonify({"error": "El campo 'texto' es obligatorio y debe ser una cadena no vacía."}), 400

    # Validar nivel
    nivel = data.get("resumen_nivel", 30)
    try:
        nivel = float(nivel)
    except:
        return jsonify({"error": "El campo 'resumen_nivel' debe ser numérico (0–100)."}), 400
    if not (0 <= nivel <= 100):
        return jsonify({"error": "El campo 'resumen_nivel' debe estar entre 0 y 100."}), 400
    porcentaje = max(0.1, min(1.0, nivel / 100.0))

    # Validar idioma pedido
    lang = data.get("lang", "es").lower()
    if lang not in ("es", "en"):
        return jsonify({"error": f"El campo 'lang' debe ser 'es' o 'en'. Se recibió '{lang}'."}), 400

    # Detectar idioma aproximado del texto
    lang_detectado = detectar_idioma_simple(texto)
    if lang_detectado in ("es", "en") and lang_detectado != lang:
        return jsonify({
            "error": f"Idioma detectado en el texto: '{lang_detectado}', pero se solicitó resumir como '{lang}'."
        }), 400

    # Llamamos a la función de resumen (debug=True para campos intermedios)
    resultado = analizar_texto(texto, porcentaje, lang=lang, debug=True)
    return jsonify(resultado), 200


@app.route("/analizar_pdf", methods=["POST"])
def analizar_pdf():
    """
    Endpoint multipart/form-data para resumir un PDF.
    Form-data esperado:
      - 'pdf' (file)            → archivo .pdf
      - 'resumen_nivel' (text)  → porcentaje (0–100)
      - 'lang' (text) opcional → "es" o "en" (por defecto "es")
    """
    # 1) Verificar que haya un archivo en 'pdf'
    if "pdf" not in request.files:
        return jsonify({"error": "No se recibió ningún archivo PDF en el campo 'pdf'."}), 400

    archivo = request.files["pdf"]
    if archivo.filename == "":
        return jsonify({"error": "El nombre del archivo PDF está vacío."}), 400

    # 2) Verificar extensión .pdf
    filename = archivo.filename.lower()
    if not filename.endswith(".pdf"):
        return jsonify({"error": "El archivo subido no tiene extensión '.pdf'."}), 400

    # 3) Extraer texto con PyPDF2
    try:
        reader = PdfReader(archivo.stream)
        paginas = []
        for p in reader.pages:
            text_p = p.extract_text() or ""
            paginas.append(text_p)
        texto_plano = "\n".join(paginas).strip()
        if texto_plano == "":
            raise ValueError("El PDF no contiene texto extractable.")
    except Exception as e:
        return jsonify({"error": f"No se pudo extraer texto del PDF: {e}"}), 500

    # 4) Validar nivel de resumen
    nivel = request.form.get("resumen_nivel", "30")
    try:
        nivel = float(nivel)
    except:
        return jsonify({"error": "El campo 'resumen_nivel' debe ser numérico (0–100)."}), 400
    if not (0 <= nivel <= 100):
        return jsonify({"error": "El campo 'resumen_nivel' debe estar entre 0 y 100."}), 400
    porcentaje = max(0.1, min(1.0, nivel / 100.0))

    # 5) Validar idioma pedido
    lang = request.form.get("lang", "es").lower()
    if lang not in ("es", "en"):
        return jsonify({"error": f"El campo 'lang' debe ser 'es' o 'en'. Se recibió '{lang}'."}), 400

    # 6) Detectar idioma aproximado en el texto extraído
    lang_detectado = detectar_idioma_simple(texto_plano)
    if lang_detectado in ("es", "en") and lang_detectado != lang:
        return jsonify({
            "error": f"Idioma detectado en el PDF: '{lang_detectado}', pero se solicitó resumir como '{lang}'."
        }), 400

    # 7) Llamar a analizar_texto sobre el texto extraído
    resultado = analizar_texto(texto_plano, porcentaje, lang=lang, debug=True)
    return jsonify(resultado), 200


if __name__ == "__main__":
    # Ejecutar en modo DEBUG en localhost:5000
    app.run(debug=True)
