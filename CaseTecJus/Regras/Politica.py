from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ItemPolitica:
    id: str
    texto: str


# Política (fictícia) — base para RAG
ITENS_POLITICA: List[ItemPolitica] = [
    ItemPolitica("POL-1", "Só compramos crédito de processos transitados em julgado e em fase de execução."),
    ItemPolitica("POL-2", "Exigir valor de condenação informado."),
    ItemPolitica("POL-3", "Valor de condenação inferior a R$ 1.000,00 não compramos."),
    ItemPolitica("POL-4", "Condenações na esfera trabalhista não compramos."),
    ItemPolitica("POL-5", "Óbito do autor sem habilitação no inventário não compramos."),
    ItemPolitica("POL-6", "Substabelecimento sem reserva de poderes não compramos."),
    ItemPolitica("POL-7", "Informar honorários contratuais, periciais e sucumbenciais quando existirem."),
    ItemPolitica("POL-8", "Se faltar documento essencial (ex.: trânsito em julgado não comprovado) → incomplete."),
]

# Compatibilidade com código anterior (se existir)
POLICY_ITEMS = ITENS_POLITICA


