<<<<<<< HEAD
﻿from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import sys

PASTA_SRC = Path(__file__).resolve().parent
PASTA_SRC_ANINHADA = PASTA_SRC / "src"

for caminho in (PASTA_SRC, PASTA_SRC_ANINHADA):
    if caminho.exists() and str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))

from parser import interpretar_mensagem
from sheets import registrar_lancamento, consultar_resumo


class WebhookHandler(BaseHTTPRequestHandler):
    def _enviar_json(self, status_code: int, payload: dict) -> None:
        corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self) -> None:
        if self.path != "/webhook":
            self._enviar_json(404, {"erro": "Rota não encontrada"})
            return

        tamanho = int(self.headers.get("Content-Length", 0))
        corpo_bruto = self.rfile.read(tamanho)

        try:
            dados = json.loads(corpo_bruto.decode("utf-8"))
        except Exception:
            self._enviar_json(400, {"erro": "JSON inválido"})
            return

        mensagem = str(dados.get("mensagem", "")).strip()
        if not mensagem:
            self._enviar_json(400, {"erro": "Campo 'mensagem' obrigatório"})
            return

        if any(termo in mensagem.lower() for termo in ("resumo", "saldo", "caixa")):
            resumo = consultar_resumo()
            self._enviar_json(200, {"tipo_resposta": "resumo", "resumo": resumo})
            return

        lancamento = interpretar_mensagem(mensagem)
        if not lancamento:
            self._enviar_json(
                200,
                {
                    "tipo_resposta": "nao_entendido",
                    "mensagem_recebida": mensagem,
                    "sugestao": "Ex.: 'recebi 150 pix cliente João' ou 'paguei 80 internet'",
                },
            )
            return

        registro = registrar_lancamento(lancamento)
        self._enviar_json(200, {"tipo_resposta": "lancamento_registrado", "registro": registro})


def main() -> None:
    servidor = HTTPServer(("127.0.0.1", 8000), WebhookHandler)
    print("Webhook rodando em http://127.0.0.1:8000/webhook")
    servidor.serve_forever()


if __name__ == "__main__":
    main()
=======
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
>>>>>>> 561b95c3dde2b9b41385781f7891dfa9d9d358b9
