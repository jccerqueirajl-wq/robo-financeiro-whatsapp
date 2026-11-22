from fastapi import FastAPI
from pydantic import BaseModel

from src.service import processar_mensagem

app = FastAPI(title="Robô Financeiro Webhook")


class MensagemEntrada(BaseModel):
    mensagem: str
    remetente: str | None = "whatsapp-simulado"


@app.post("/webhook/whatsapp")
def receber_mensagem(payload: MensagemEntrada) -> dict:
    resposta, encerrar = processar_mensagem(
        payload.mensagem,
        remetente=payload.remetente,
    )
    return {
        "remetente": payload.remetente,
        "resposta": resposta,
        "encerrar": encerrar,
    }