from src.service import processar_mensagem


def executar_simulador() -> None:
    print("Simulador do Robô Financeiro iniciado. Digite 'resumo', 'ajuda' ou 'sair'.")

    while True:
        try:
            entrada = input("\nVocê: ")
        except (KeyboardInterrupt, EOFError):
            print("\nRobô: Até mais!")
            break

        resposta, encerrar = processar_mensagem(entrada, remetente="cli-local")
        print(f"Robô: {resposta}")

        if encerrar:
            break


if __name__ == "__main__":
    executar_simulador()