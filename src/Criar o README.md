# Robô Financeiro WhatsApp

Protótipo em Python para registrar entradas e saídas financeiras a partir de mensagens de texto, armazenar o fluxo de caixa em arquivo CSV e consultar o resumo financeiro (`entradas`, `saídas` e `saldo`). Atualmente conta com um simulador interativo no terminal, preparado para futura integração com API de WhatsApp.

## Estrutura do Projeto

```text
robo-financeiro-whatsapp/
├── .gitignore
├── README.md
├── data/
│   └── fluxo_caixa.csv      # Gerado automaticamente (ignorado pelo Git)
└── src/
    ├── __init__.py
    ├── parser.py            # Interpreta mensagens e extrai tipo, valor, categoria e descrição
    ├── sheets.py            # Cria/atualiza o CSV e calcula o resumo financeiro
    └── main.py              # Simulador interativo via terminal (CLI)