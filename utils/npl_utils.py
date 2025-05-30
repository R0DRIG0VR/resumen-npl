import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.blank("es")
nlp.add_pipe("sentencizer")

def limpiar_texto(texto):
    doc = nlp(texto.lower())
    return [token.text for token in doc if token.is_alpha]

def filtrar_redundancia(oraciones, tfidf, umbral=0.8):
    seleccionadas = []
    for o in oraciones:
        if all(cosine_similarity(tfidf.transform([o]), tfidf.transform([s]))[0][0] < umbral for s in seleccionadas):
            seleccionadas.append(o)
    return seleccionadas

def seleccionar_mmr(oraciones, matriz, n, lambda_=0.7):
    seleccionadas = []
    indices_disponibles = list(range(len(oraciones)))
    puntuaciones_mmr = []

    while len(seleccionadas) < n and indices_disponibles:
        mejor_idx = None
        mejor_valor = -np.inf

        for i in indices_disponibles:
            sim_doc = cosine_similarity(matriz[i], np.asarray(matriz.mean(axis=0)))[0][0]
            sim_redund = max(
                cosine_similarity(matriz[i], matriz[j])[0][0]
                for j in seleccionadas
            ) if seleccionadas else 0
            score = lambda_ * sim_doc - (1 - lambda_) * sim_redund

            if score > mejor_valor:
                mejor_valor = score
                mejor_idx = i

        puntuaciones_mmr.append({
            "oracion": oraciones[mejor_idx],
            "indice": mejor_idx,
            "score": mejor_valor
        })

        seleccionadas.append(mejor_idx)
        indices_disponibles.remove(mejor_idx)

    return [oraciones[i] for i in seleccionadas], puntuaciones_mmr

def obtener_top_tfidf(matriz, tfidf, oraciones, top_n=3):
    nombres = tfidf.get_feature_names_out()
    pesos = matriz.toarray()
    resultados = []
    for idx, row in enumerate(pesos):
        top_idxs = row.argsort()[::-1][:top_n]
        top_terms = [(nombres[i], round(row[i], 3)) for i in top_idxs]
        resultados.append({"oracion": oraciones[idx], "top_tfidf": top_terms})
    return resultados

def resumir_texto(texto, porcentaje=0.3, min_oraciones=1, max_oraciones=15, debug=False):
    doc = nlp(texto)
    oraciones = [sent.text.strip() for sent in doc.sents]
    total = len(oraciones)

    if total <= min_oraciones:
        return {"resumen": texto}

    n = max(min_oraciones, min(max_oraciones, int(total * porcentaje)))
    tfidf = TfidfVectorizer()
    matriz = tfidf.fit_transform(oraciones)

    seleccionadas_mmr, puntuaciones_mmr = seleccionar_mmr(oraciones, matriz, n)
    resumen_final = filtrar_redundancia(seleccionadas_mmr, tfidf)

    # Devolver solo el resumen final bajo el campo "resumen"
    resumen_data = {
        "resumen": " ".join(resumen_final)
    }

    if debug:
        resumen_data.update({
            "oraciones_segmentadas": oraciones,
            "top_palabras_por_oracion": obtener_top_tfidf(matriz, tfidf, oraciones),
            "oraciones_mmr": seleccionadas_mmr,
            "puntuaciones_mmr": puntuaciones_mmr
        })

    return resumen_data

def analizar_texto(texto, porcentaje=0.3, debug=False):
    tokens = limpiar_texto(texto)
    resumen_info = resumir_texto(texto, porcentaje, debug=debug)
    resumen_info["tokens_limpios"] = tokens
    return resumen_info
