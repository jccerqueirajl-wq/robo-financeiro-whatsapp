import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Garante que tanto 'src/' quanto 'src/src/' sejam encontrados nas importações
DIRETORIO_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRETORIO_SRC))
sys.path.insert(0, str(DIRETORIO_SRC / "src"))

from parser import interpretar_mensagem
from sheets import consultar_resumo, registrar_lancamento


class WebhookWhatsAppHandler(BaseHTTPRequestHandler):
    """Manipulador HTTP para simular o recebimento de mensagens do WhatsApp."""

    def _enviar_json(self, status_code: int, payload: dict) -> None:
        resposta_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resposta_bytes)))
        self.end_headers()
        self.wfile.write(resposta_bytes)

    def do_GET(self) -> None:
        """Rota simples de healthcheck e verificação do webhook."""
        if self.path == "/health":
            self._enviar_json(200, {"status": "online", "servico": "robo-financeiro-whatsapp"})
        else:
            self._enviar_json(404, {"erro": "Rota não encontrada. Use POST /webhook ou GET /health"})

    def do_POST(self) -> None:
        """Recebe payload JSON com 'mensagem', processa e atualiza a planilha."""
        if self.path != "/webhook":
            self._enviar_json(404, {"erro": "Endpoint inválido. Envie POST para /webhook"})
            return

        try:
            tamanho_conteudo = int(self.headers.get("Content-Length", 0))
            corpo_bruto = self.rfile.read(tamanho_conteudo).decode("utf-8")
            dados = json.loads(corpo_bruto) if corpo_bruto else {}
        except (ValueError, json.JSONDecodeError):
            self._enviar_json(400, {"erro": "JSON inválido no corpo da requisição."})
            return

        mensagem = str(dados.get("mensagem", "")).strip()
        if not mensagem:
            self._enviar_json(400, {"erro": "Campo 'mensagem' é obrigatório."})
            return

        # 1. Verifica se o usuário pediu resumo/saldo
        if any(palavra in mensagem.lower() for palavra in ("resumo", "saldo", "extrato", "total")):
            resumo = consultar_resumo()
            resposta_bot = (
                f"📊 *Resumo do Caixa*\n"
                f"Entradas: R$ {resumo['entradas']:.2f}\n"
                f"Saídas: R$ {resumo['saidas']:.2f}\n"
                f"Saldo atual: R$ {resumo['saldo']:.2f}"
            )
            self._enviar_json(200, {"acao": "consulta", "resumo": resumo, "resposta_whatsapp": resposta_bot})
            return

        # 2. Tenta interpretar como lançamento financeiro (entrada/saída)
        lancamento = interpretar_mensagem(mensagem)
        if not lancamento:
            self._enviar_json(
                200,
                {
                    "acao": "nao_compreendido",
                    "resposta_whatsapp": (
                        "Não consegui entender o lançamento. "
                        "Tente algo como: 'recebi 150 pix cliente João' ou 'paguei 80 internet'."
                    ),
                },
            )
            return

        # 3. Grava na planilha CSV e retorna confirmação
        registro = registrar_lancamento(lancamento)
        sinal = "+" if registro["tipo"] == "entrada" else "-"
        resposta_bot = (
            f"✅ *Lançamento registrado!*\n"
            f"Tipo: {registro['tipo'].capitalize()}\n"
            f"Valor: {sinal} R$ {registro['valor']:.2f}\n"
            f"Categoria: {registro['categoria']}\n"
            f"Descrição: {registro['descricao']}"
        )

        self._enviar_json(
            200,
            {
                "acao": "lancamento_registrado",
                "registro": registro,
                "resposta_whatsapp": resposta_bot,
            },
        )


def iniciar_servidor(host: str = "127.0.0.1", porta: int = 8000) -> None:
    servidor = HTTPServer((host, porta), WebhookWhatsAppHandler)
    print(f"Webhook rodando em http://{host}:{porta}/webhook (Ctrl+C para encerrar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()