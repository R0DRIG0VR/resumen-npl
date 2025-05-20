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

        seleccionadas.append(mejor_idx)
        indices_disponibles.remove(mejor_idx)

    return [oraciones[i] for i in seleccionadas]

def resumir_texto(texto, porcentaje=0.3, min_oraciones=1, max_oraciones=15):
    doc = nlp(texto)
    oraciones = [sent.text.strip() for sent in doc.sents]
    total = len(oraciones)

    if total <= min_oraciones:
        return texto

    n = max(min_oraciones, min(max_oraciones, int(total * porcentaje)))

    # TF-IDF vectorización
    tfidf = TfidfVectorizer()
    matriz = tfidf.fit_transform(oraciones)

    # Selección MMR
    seleccionadas = seleccionar_mmr(oraciones, matriz, n)

    # Filtro de redundancia
    seleccionadas = filtrar_redundancia(seleccionadas, tfidf)

    return " ".join(seleccionadas)

def analizar_texto(texto, porcentaje=0.3):
    tokens = limpiar_texto(texto)
    resumen = resumir_texto(texto, porcentaje)
    return {
        "resumen": resumen,
        "tokens_limpios": tokens,
    }
