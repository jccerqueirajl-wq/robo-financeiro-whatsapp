from src.parser import interpretar_mensagem
from src.sheets import consultar_resumo, registrar_lancamento


def responder_mensagem(texto: str) -> str:
    comando = texto.strip().lower()

    if comando in ("resumo", "saldo", "/resumo", "/saldo"):
        resumo = consultar_resumo()
        return (
            f"Resumo financeiro:\n"
            f"- Entradas: R$ {resumo['entradas']:.2f}\n"
            f"- Saídas: R$ {resumo['saidas']:.2f}\n"
            f"- Saldo: R$ {resumo['saldo']:.2f}"
        )

    lancamento = interpretar_mensagem(texto)
    if not lancamento:
        return (
            "Não consegui entender esse lançamento. "
            "Tente algo como: 'recebi 150 pix cliente João' ou 'paguei 80 internet' "
            "(ou digite 'resumo')."
        )

    salvo = registrar_lancamento(lancamento)
    sinal = "+" if salvo["tipo"] == "entrada" else "-"
    return (
        f"Registrado ({salvo['tipo']}): {sinal}R$ {salvo['valor']:.2f} "
        f"[{salvo['categoria']}] - {salvo['descricao']}"
    )


def iniciar_simulador() -> None:
    print("Simulador do Robô Financeiro iniciado. Digite 'resumo' ou 'sair'.")
    while True:
        try:
            mensagem = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando simulador.")
            break

        if not mensagem:
            continue

        if mensagem.lower() in ("sair", "exit", "/sair"):
            print("Robô: Até mais!")
            break

        resposta = responder_mensagem(mensagem)
        print(f"Robô:\n{resposta}")


if __name__ == "__main__":
    iniciar_simulador()