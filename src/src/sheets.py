import csv
from datetime import datetime
from pathlib import Path

CAMINHO_PLANILHA = Path("data/fluxo_caixa.csv")
CABECALHO = ["data_hora", "tipo", "categoria", "valor", "descricao"]


def garantir_planilha() -> None:
    CAMINHO_PLANILHA.parent.mkdir(parents=True, exist_ok=True)
    if not CAMINHO_PLANILHA.exists():
        with CAMINHO_PLANILHA.open("w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(CABECALHO)


def registrar_lancamento(lancamento: dict) -> dict:
    garantir_planilha()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha = [
        agora,
        lancamento["tipo"],
        lancamento["categoria"],
        f"{lancamento['valor']:.2f}",
        lancamento["descricao"],
    ]

    with CAMINHO_PLANILHA.open("a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(linha)

    return {
        "data_hora": agora,
        "tipo": lancamento["tipo"],
        "categoria": lancamento["categoria"],
        "valor": lancamento["valor"],
        "descricao": lancamento["descricao"],
    }


def consultar_resumo() -> dict:
    garantir_planilha()
    entradas = 0.0
    saidas = 0.0

    with CAMINHO_PLANILHA.open("r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for linha in leitor:
            valor = float(linha["valor"])
            if linha["tipo"] == "entrada":
                entradas += valor
            elif linha["tipo"] == "saida":
                saidas += valor

    saldo = entradas - saidas
    return {
        "entradas": entradas,
        "saidas": saidas,
        "saldo": saldo,
    }