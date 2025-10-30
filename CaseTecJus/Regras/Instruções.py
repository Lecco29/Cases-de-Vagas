import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from .modelos import Processo, DecisionOutput
from .rag import recuperar_trechos_politica


def _obter_cliente() -> OpenAI:
    url_base = os.getenv("OPENAI_BASE_URL")
    if url_base:
        return OpenAI(base_url=url_base)
    return OpenAI()


cliente_ia = _obter_cliente()

INSTRUCOES_SISTEMA = (
    "Você é um verificador de processos judiciais. "
    "Use a Política da Empresa (POL-*) para decidir entre approved, rejected ou incomplete. "
    "A saída DEVE ser exclusivamente JSON válido com os campos: decision, rationale, citations (ex.: ['POL-1']). "
    "Nunca produza texto fora do JSON."
)


def construir_contexto(processo: Processo) -> Dict[str, Any]:
    documentos_compactados = [
        {
            "id": doc.id,
            "dataHoraJuntada": doc.dataHoraJuntada.isoformat(),
            "nome": doc.nome,
        }
        for doc in processo.documentos
    ]
    movimentos_compactados = [
        {
            "dataHora": mov.dataHora.isoformat(),
            "descricao": mov.descricao,
        }
        for mov in processo.movimentos
    ]
    return {
        "numeroProcesso": processo.numeroProcesso,
        "classe": processo.classe,
        "orgaoJulgador": processo.orgaoJulgador,
        "ultimaDistribuicao": processo.ultimaDistribuicao.isoformat(),
        "assunto": processo.assunto,
        "segredoJustica": processo.segredoJustica,
        "justicaGratuita": processo.justicaGratuita,
        "siglaTribunal": processo.siglaTribunal,
        "esfera": processo.esfera,
        "documentos": documentos_compactados,
        "movimentos": movimentos_compactados,
    }


def recuperar_politica_com_consulta(processo: Processo) -> List[Dict[str, Any]]:
    partes = [
        processo.classe,
        processo.assunto,
        processo.esfera,
        ", ".join(doc.nome for doc in processo.documentos[:3]),
        ", ".join(mov.descricao for mov in processo.movimentos[-3:]),
    ]
    consulta = " | ".join([p for p in partes if p])
    resultados = recuperar_trechos_politica(consulta, k=5)
    return [
        {"id": id_pol, "text": texto_pol, "score": score}
        for id_pol, texto_pol, score in resultados
    ]


def decidir(processo: Processo) -> DecisionOutput:
    contexto = construir_contexto(processo)
    politica_ctx = recuperar_politica_com_consulta(processo)

    esquema_saida = {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["approved", "rejected", "incomplete"],
            },
            "rationale": {"type": "string"},
            "citations": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["decision", "rationale", "citations"],
        "additionalProperties": False,
    }

    mensagens = [
        {"role": "system", "content": INSTRUCOES_SISTEMA},
        {
            "role": "user",
            "content": (
                "Política relevante (RAG):\n" +
                json.dumps(politica_ctx, ensure_ascii=False, indent=2) +
                "\n\nProcesso:\n" +
                json.dumps(contexto, ensure_ascii=False, indent=2) +
                "\n\nResponda apenas com JSON válido no formato especificado."
            ),
        },
    ]

    resposta = cliente_ia.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=mensagens,
        response_format={"type": "json_schema", "json_schema": {"name": "Decision", "schema": esquema_saida}},
        temperature=0.0,
    )

    conteudo = resposta.choices[0].message.content
    dados = json.loads(conteudo)
    return DecisionOutput(**dados)


