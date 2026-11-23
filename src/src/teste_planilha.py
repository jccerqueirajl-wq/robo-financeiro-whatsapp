from pathlib import Path
import sys

# Garante que 'src' seja encontrado ao rodar na raiz
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from sheets import registrar_lancamento, consultar_resumo, CAMINHO_PLANILHA


def rodar_teste_persistencia():
    # Opcional: remove o arquivo de teste anterior para começar limpo
    if CAMINHO_PLANILHA.exists():
        CAMINHO_PLANILHA.unlink()

    r1 = registrar_lancamento({
        "tipo": "entrada",
        "categoria": "pix",
        "valor": 150.0,
        "descricao": "recebi 150 pix cliente João",
    })
    r2 = registrar_lancamento({
        "tipo": "saida",
        "categoria": "internet",
        "valor": 85.5,
        "descricao": "pagamento conta internet",
    })

    resumo = consultar_resumo()

    print("Lançamento 1:", r1)
    print("Lançamento 2:", r2)
    print("Resumo:", resumo)

    assert resumo["entradas"] == 150.0
    assert resumo["saidas"] == 85.5
    assert resumo["saldo"] == 64.5
    print("Teste de persistência concluído com sucesso!")


if __name__ == "__main__":
    rodar_teste_persistencia()