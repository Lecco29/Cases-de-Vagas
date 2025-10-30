from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, Field


class Documento(BaseModel):
    id: str
    dataHoraJuntada: datetime
    nome: str
    texto: str


class Movimento(BaseModel):
    dataHora: datetime
    descricao: str


class Processo(BaseModel):
    numeroProcesso: str
    classe: str
    orgaoJulgador: str
    ultimaDistribuicao: datetime
    assunto: str
    segredoJustica: bool
    justicaGratuita: bool
    siglaTribunal: str
    esfera: str
    documentos: List[Documento]
    movimentos: List[Movimento]


class DecisionOutput(BaseModel):
    # Mantemos os campos em inglês para cumprir o contrato de saída do case
    decision: Literal["approved", "rejected", "incomplete"]
    rationale: str = Field(..., description="Justificativa clara e objetiva para a decisão")
    citations: List[str] = Field(
        default_factory=list,
        description="Lista de IDs de política utilizados, ex.: ['POL-1','POL-2']",
    )


