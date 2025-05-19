import spacy
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

nlp = spacy.load("es_core_news_sm")

def limpiar_texto(texto):
    doc = nlp(texto.lower())
    palabras_limpias = [
        token.text for token in doc
        if token.is_alpha and not token.is_stop
    ]
    return palabras_limpias

def vectorizar_oraciones(oraciones):
    return [nlp(oracion).vector for oracion in oraciones]

def resumir_texto(texto, n_oraciones=3):
    doc = nlp(texto)
    oraciones = [sent.text.strip() for sent in doc.sents if len(sent.text.strip().split()) > 4]

    if len(oraciones) <= n_oraciones:
        return texto

    vectores = vectorizar_oraciones(oraciones)

    # Crear matriz de similitud
    sim_matrix = cosine_similarity(vectores)

    # Crear grafo y aplicar PageRank
    grafo = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(grafo)

    # Ordenar oraciones por score de TextRank
    oraciones_ordenadas = sorted(
        ((scores[i], oracion) for i, oracion in enumerate(oraciones)),
        reverse=True
    )

    resumen = " ".join([oracion for _, oracion in oraciones_ordenadas[:n_oraciones]])
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
