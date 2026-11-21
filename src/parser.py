import re


def interpretar_mensagem(texto: str) -> dict | None:
    """
    Interpreta comandos financeiros simples enviados por mensagem.
    Exemplos:
      - "recebi 150 pix cliente João"
      - "paguei 80 internet"
    """
    if not texto or not texto.strip():
        return None

    texto_limpo = texto.strip()
    texto_minusculo = texto_limpo.lower()

    # Identifica se é entrada (recebimento / Pix) ou saída (pagamento / despesa)
    palavras_entrada = ("recebi", "recebido", "entrada", "pix recebido", "venda")
    palavras_saida = ("paguei", "pago", "saída", "saida", "despesa", "gastei")

    if any(palavra in texto_minusculo for palavra in palavras_entrada):
        tipo = "entrada"
    elif any(palavra in texto_minusculo for palavra in palavras_saida):
        tipo = "saida"
    else:
        return None

    # Procura o primeiro número (ex: 150, 150.50 ou 150,50)
    match_valor = re.search(r"(\d+(?:[.,]\d{1,2})?)", texto_minusculo)
    if not match_valor:
        return None

    valor_str = match_valor.group(1).replace(",", ".")
    valor = float(valor_str)

    # Identifica meio de pagamento/categoria básica
    if "pix" in texto_minusculo:
        categoria = "pix"
    elif "internet" in texto_minusculo:
        categoria = "internet"
    elif "luz" in texto_minusculo or "energia" in texto_minusculo:
        categoria = "energia"
    elif "aluguel" in texto_minusculo:
        categoria = "aluguel"
    else:
        categoria = "geral"

    return {
        "tipo": tipo,
        "valor": valor,
        "categoria": categoria,
        "descricao": texto_limpo,
    }