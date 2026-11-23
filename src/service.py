from src.parser import interpretar_mensagem
from src.sheets import consultar_resumo, registrar_lancamento


def processar_mensagem(texto: str, remetente: str | None = None) -> tuple[str, bool]:
    _ = remetente

    if not texto or not texto.strip():
        return "Envie um lançamento (ex.: 'recebi 150 pix cliente João') ou digite 'resumo'.", False

    comando = texto.strip().lower()

    if comando in ("sair", "exit", "quit"):
        return "Até mais!", True

    if comando in ("ajuda", "help", "/ajuda", "/help"):
        return (
            "Comandos disponíveis:\n"
            "- Registrar entrada: 'recebi 50 pix venda'\n"
            "- Registrar saída: 'paguei 80 internet'\n"
            "- Ver totais: 'resumo'\n"
            "- Encerrar (no simulador): 'sair'"
        ), False

    if comando in ("resumo", "saldo", "/resumo", "/saldo"):
        resumo = consultar_resumo()
        return (
            "Resumo financeiro:\n"
            f"- Entradas: R$ {resumo['entradas']:.2f}\n"
            f"- Saídas: R$ {resumo['saidas']:.2f}\n"
            f"- Saldo: R$ {resumo['saldo']:.2f}"
        ), False

    lancamento = interpretar_mensagem(texto)
    if not lancamento:
        return (
            "Não entendi a mensagem. Tente algo como 'recebi 150 pix cliente João' "
            "ou 'paguei 80 internet', ou digite 'resumo'."
        ), False

    registrar_lancamento(lancamento)
    sinal = "+" if lancamento["tipo"] == "entrada" else "-"
    return (
        f"Registrado ({lancamento['tipo']}): {sinal}R$ {lancamento['valor']:.2f} "
        f"[categoria: {lancamento['categoria']}]"
    ), False
