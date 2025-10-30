import os
from typing import List, Tuple

import numpy as np
from openai import OpenAI

from .Politica import ITENS_POLITICA


def _get_client() -> OpenAI:
    # OPENAI_API_KEY must be set by environment
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(base_url=base_url)
    return OpenAI()


_client = _get_client()


def _embed_texts(texts: List[str]) -> np.ndarray:
    # Uses text-embedding-3-small for cost/latency balance
    response = _client.embeddings.create(model="text-embedding-3-small", input=texts)
    vectors = [np.array(d.embedding, dtype=np.float32) for d in response.data]
    return np.vstack(vectors)


_textos_politica = [f"{p.id}: {p.texto}" for p in ITENS_POLITICA]
_ids_politica = [p.id for p in ITENS_POLITICA]
_matriz_politica = _embed_texts(_textos_politica)
_normas_politica = np.linalg.norm(_matriz_politica, axis=1, keepdims=True) + 1e-9


def recuperar_trechos_politica(consulta: str, k: int = 5) -> List[Tuple[str, str, float]]:
    vetor_consulta = _embed_texts([consulta])[0]
    vetor_consulta = vetor_consulta / (np.linalg.norm(vetor_consulta) + 1e-9)
    pontuacoes = (_matriz_politica / _normas_politica.squeeze()) @ vetor_consulta
    idx = np.argsort(-pontuacoes)[:k]
    resultados: List[Tuple[str, str, float]] = []
    for i in idx:
        resultados.append((_ids_politica[i], _textos_politica[i], float(pontuacoes[i])))
    return resultados


