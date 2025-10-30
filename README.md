# Verificador de Processos Judiciais 

Aplicação que recebe dados de um processo judicial, valida a conformidade com a Política da Empresa usando LLM (OpenAI) com RAG e retorna decisão estruturada em JSON. Disponibiliza API (FastAPI) e UI simples (Streamlit).

## Requisitos
- Python 3.11+
- Chave de API da OpenAI em `OPENAI_API_KEY`

Opcional:
- `OPENAI_BASE_URL` para compatibilidade com proxies/routers
- `OPENAI_MODEL` (padrão: `gpt-4o-mini`)

## Executar localmente
1. Crie e exporte as variáveis de ambiente:
   ```bash
   # PowerShell
   $env:OPENAI_API_KEY="SEU_TOKEN"
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute API e UI:
   ```bash
   uvicorn Regras.api:app --reload --port 8000
   # em outro terminal
   streamlit run Interface/streamlit_app.py
   ```
4. Acesse:
   - API docs (Swagger): `http://localhost:8000/docs`
   - Health: `http://localhost:8000/health`
   - UI: `http://localhost:8501`



## Deploy 
- Crie um novo serviço a partir do Dockerfile deste repositório
- Defina variáveis de ambiente:
  - `OPENAI_API_KEY` (obrigatória)
  - `OPENAI_MODEL` (opcional)
  - `OPENAI_BASE_URL` (opcional)
- Exponha portas 8000 (API) e 8501 (UI)
- Use o comando padrão do Dockerfile (não precisa alterar)

Links esperados em produção:
- API: `https://SEU_HOST/` (Swagger em `/docs`, health em `/health`)
- UI: `https://SEU_HOST:8501/` (ou conforme proxy de portas do provedor)

## Contrato de Entrada 
Veja `Regras/modelos.py` para o schema. Exemplo mínimo aceito pela UI em `Interface/streamlit_app.py`.

## Saída (sempre JSON)
```json
{
  "decision": "approved|rejected|incomplete",
  "rationale": "Justificativa clara",
  "citations": ["POL-1", "POL-2"]
}
```

## Observabilidade e Boas Práticas
- Logs padrão via servidor 
- Prompts consolidados no `Regras/Instruções.py` com formatação JSON estrita
- RAG simples com embeddings da política (`Regras/rag.py`)


## Endpoints
- `GET /health` → `{ "status": "ok" }`
- `POST /decide` → body `Processo` e resposta `DecisionOutput`
- Swagger/OpenAPI: `/docs`

## Orquestração
- Recomendada integração com LangSmith/Langfuse para rastreamento de execuções (opcional)

## Licença
Uso para o case técnico.
