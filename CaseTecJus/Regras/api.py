import os
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .Instruções import decidir
from .modelos import Processo, DecisionOutput

load_dotenv()  # carrega variáveis do .env se presente

app = FastAPI(title="Verificador de Processos Judiciais", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/decide", response_model=DecisionOutput)
def post_decide(processo: Processo) -> DecisionOutput:
    try:
        result = decidir(processo)
        return JSONResponse(content=result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


