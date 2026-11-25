# Bancada do Jev (teste só no PC)

Teste do Jev (TypeSafe) como segunda barreira da Clara. **Não toca** no n8n, no servidor, nos bancos nem no WhatsApp. Só usa conversas inventadas.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `RESULTADO.md` | **Comece por aqui.** Resumo, tabela, limiares e recomendação. |
| `jev_bancada.py` | O script. Monta os casos, chama o Jev e conta os acertos. |
| `jev_resultados.json` | Resposta crua do Jev em cada caso (sem a chave). |
| `jev_experimento_cancelar.json` | Segundo teste, só do cancelar (3 perguntas). |
| `analise.txt` | Saída completa da conta de acertos e limiares. |

## Como rodar de novo

Dentro de `tecnico/jev-bancada`:

```powershell
python jev_bancada.py rodar
```

Chama o Jev (custa menos de US$ 0,02 e leva uns 2 minutos). Só chama o que ainda não está em `jev_resultados.json`.

```powershell
python jev_bancada.py analisar
```

Refaz as contas sem chamar nada (grátis).

```powershell
python jev_bancada.py cancelar2
```

Refaz o teste do cancelar com 3 perguntas (custa cerca de US$ 0,002).

## Cuidados

- A chave `TYPESAFE_API_KEY` é lida do `.env` da raiz, só dentro do script. Ela não é impressa nem gravada em nenhum arquivo daqui.
- Só conversas inventadas (`tecnico/teste-ab/paciente-simulado-20261124-214610.json`) e os casos de teste do Pacote C e do Codex. Nada de paciente real.
- Os rótulos de "o que seria certo" foram feitos à mão e estão no script (`GOLD`). Revise antes de tomar decisão grande.
