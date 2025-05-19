import spacy
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

nlp = spacy.load("es_core_news_sm")


def limpiar_texto(texto):
    doc = nlp(texto.lower())
    palabras_limpias = [
        token.text for token in doc
        if token.is_alpha and not token.is_stop
    ]
    return palabras_limpias


def resumir_texto(texto, n_oraciones=3):
    doc = nlp(texto)
    oraciones = list(doc.sents)

    if len(oraciones) <= n_oraciones:
        return texto  # No resumir si el texto es corto

    # Obtener vectores de cada oración
    vectores = [oracion.vector for oracion in oraciones]

    # Calcular el vector promedio del documento
    vector_promedio = np.mean(vectores, axis=0).reshape(1, -1)

    # Calcular la similitud de cada oración con el tema general
    similitudes = [
        cosine_similarity([v.reshape(1, -1)[0]], vector_promedio)[0][0]
        for v in vectores
    ]

    # Ordenar oraciones por similitud
    oraciones_ordenadas = [
        oracion for _, oracion in sorted(zip(similitudes, oraciones), reverse=True)
    ]

    # Seleccionar las más representativas
    resumen = " ".join([oracion.text for oracion in oraciones_ordenadas[:n_oraciones]])
    return resumen


def analizar_texto(texto):
    doc = nlp(texto)
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    tokens = limpiar_texto(texto)
    resumen = resumir_texto(texto)
    return {
        "resumen": resumen,
        "tokens_limpios": tokens,
        "entidades": entidades
    }
