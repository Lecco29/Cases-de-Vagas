import json
import os

import requests
import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Verificador de Processos", page_icon="⚖️", layout="centered")
st.title("Verificador de Processos Judiciais")
st.caption("Envie os dados do processo em JSON e veja a decisão consolidada")

default_json = {
    "numeroProcesso": "0001234-56.2023.4.05.8100",
    "classe": "Cumprimento de Sentença contra a Fazenda Pública",
    "orgaoJulgador": "19ª VARA FEDERAL - SOBRAL/CE",
    "ultimaDistribuicao": "2024-11-18T23:15:44.130Z",
    "assunto": "Rural (Art. 48/51)",
    "segredoJustica": False,
    "justicaGratuita": True,
    "siglaTribunal": "TRF5",
    "esfera": "Federal",
    "documentos": [
        {
            "id": "DOC-1-1",
            "dataHoraJuntada": "2023-09-10T10:12:05.000",
            "nome": "Sentença de Mérito",
            "texto": "…",
        },
        {
            "id": "DOC-1-2",
            "dataHoraJuntada": "2023-12-12T09:05:30.000",
            "nome": "Certidão de Trânsito em Julgado",
            "texto": "…",
        },
    ],
    "movimentos": [
        {
            "dataHora": "2024-01-20T11:22:33.000",
            "descricao": "Iniciado cumprimento definitivo de sentença.",
        }
    ],
}

input_text = st.text_area("JSON do Processo", json.dumps(default_json, ensure_ascii=False, indent=2), height=400)

if st.button("Analisar", type="primary"):
    try:
        payload = json.loads(input_text)
        resp = requests.post(f"{API_URL}/decide", json=payload, timeout=90)
        if resp.status_code == 200:
            st.success("Decisão gerada")
            st.json(resp.json())
        else:
            st.error(f"Erro {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(str(e))


