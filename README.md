
# Robô Financeiro no WhatsApp

> Assistente de WhatsApp para pequenos empresários gerenciarem pagamentos, recebimentos via Pix e atualizações de planilhas por mensagens simples.

## 🎯 Objetivo
Facilitar o controle de fluxo de caixa diário sem precisar abrir o computador a cada venda ou despesa, registrando entradas, saídas e consultas diretamente em planilhas.

## ⚙️ Funcionalidades Planejadas
- **Registro de recebimentos (Pix):** Interpretar mensagens como \`recebi 150 pix cliente João\` e lançar na planilha.
- **Registro de pagamentos:** Registrar despesas e contas pagas com valor, categoria e data.
- **Execução e consulta de planilhas:** Atualizar saldos, gerar relatórios resumidos e consultar totais pelo WhatsApp.

## 🛠️ Tecnologias
- **Linguagem:** Python
- **Manipulação de Planilhas:** CSV / OpenPyXL / Google Sheets API
- **Integração WhatsApp:** Webhook / API de mensagens

## 📁 Estrutura do Projeto
- \`src/\`: Código-fonte principal do robô, interpretador de comandos e integração com planilhas.
- \`data/\`: Diretório local de armazenamento das planilhas de teste.
