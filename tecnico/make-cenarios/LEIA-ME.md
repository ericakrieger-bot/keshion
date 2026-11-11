# Cópias dos cenários do Make

Cópia de segurança dos cenários da Keshion, para restaurar ou levar para o n8n.
Última atualização: 11/11/2026.

| Arquivo | Cenário no Make | O que faz |
|---|---|---|
| `1A-entrada-8302405.json` | Keshion · 1A Entrada (WhatsApp) | Recebe do Whapi, separa texto, áudio e foto, pausa quando a doutora assume, comando #reiniciar |
| `1B-resposta-8302452.json` | Keshion · 1B Resposta (IA e modo copiloto) | Fila de 7 s, ficha, agenda, Claude Haiku, marcar, remarcar, cancelar, avisos |
| `1C-fechamento-8463643.json` | Keshion · 1C Fechamento depois da marcação | Despedida 1 minuto depois de marcar, se o paciente não respondeu |
| `1D-envio-8464848.json` | Keshion · 1D Envio (até 3 mensagens) | Envia até 3 mensagens com "digitando" e avisa a Erica se falhar |

As instruções da assistente e a base da clínica ficam no data store 240983 (registros `_instrucoes` e `_base`). As cópias em texto estão em `clientes/clinica-demo/instrucoes-sarah.md` e `clientes/clinica-demo/base-clinica.md`.

Os arquivos guardam só o número das conexões (Whapi, Google, OpenAI, Anthropic), nunca as chaves.

Para restaurar: no Make, crie um cenário novo, use "Import blueprint" e escolha o arquivo. Depois refaça as conexões e confira os webhooks.
