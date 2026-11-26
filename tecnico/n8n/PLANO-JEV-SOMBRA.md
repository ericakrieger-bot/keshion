# Jev em modo sombra (plano de 25/11/2026)

Origem: bancada do Jev (`tecnico/jev-bancada/RESULTADO.md`), aprovada pela Erica em 25/11. Privacidade dada como resolvida pela Erica.

## O que muda para o paciente

Nada. A Clara continua decidindo só com as regras de hoje. O Jev só "dá a opinião" e o fluxo anota.

## Como funciona

1. Depois que o fluxo já decidiu o que fazer ("Decidir a ação"), abre um caminho lateral que **só roda depois que a resposta do paciente já saiu**.
2. Esse caminho chama o Jev uma vez (modelo fixo `jev-1.14.0`, últimas 6 trocas da conversa), com as perguntas:
   - urgência; "dói?" x dor; fora da lista (implante, dentadura, coroa sobre implante);
   - só quando o código sabe que a última fala da Clara foi a pergunta de cancelar: confirmação, "pede para esperar" e "pede para cancelar".
3. Limite de 3 segundos. Se o Jev falhar, demorar ou responder algo estranho, o fluxo anota "falhou" e para ali. Nunca vira "não" e nunca atrapalha a resposta.
4. A chave fica numa credencial do n8n chamada "TypeSafe" (como a da Anthropic), copiada do `/opt/keshion/.env`. Sem essa credencial no `clinica.json`, o fluxo sai igual ao de hoje.

## Onde grava

Tabela nova `jev_sombra` no banco de cada clínica, uma linha por resposta da Clara:
- quando, telefone, id da mensagem, texto da mensagem do paciente (para entender as diferenças);
- o que a regra de hoje fez: urgência sim/não, caminho escolhido (responder, equipe, agenda, cancelar), confirmou cancelar ou não;
- o que o Jev diria: probabilidades de cada pergunta e a decisão que ele tomaria com os limiares do RESULTADO.md (urgência 0,3; fora da lista 0,7; "dói?" 0,67; cancelar pela regra mista);
- tempo, custo, versão do modelo, erro (se houve).
Apagar linhas com mais de 60 dias (o próprio fluxo limpa).

## O que olhar na comparação (depois de 1 a 2 semanas)

Um script (`tecnico/jev-bancada/comparar_sombra.py`) lê a tabela e mostra:
1. **Urgência:** casos em que o Jev avisaria e a regra não (o que a regra perdeu) e o contrário (alarme falso do Jev).
2. **"Dói?" e fora da lista:** onde os dois discordam, com o texto.
3. **Cancelar:** casos em que a regra de hoje perguntou de novo e o Jev cancelaria, e o contrário.
4. **Saúde:** quantas falhas, tempo médio e máximo, custo total.

Ordem para ligar de verdade: urgência, depois "dói?" e implante/dentadura, por último o cancelar.

## Como ligar no gerador (FEITO em 26/11, junto com a correção do cancelar, com OK da Erica: "Jeito 1")

Publicado na demo e na clínica de teste em 26/11, às 07h22 do servidor. Teste: `tecnico/teste-ab/PROMPT-TESTE-26-11-cancelar-e-jev.md`. Desde 26/11 o gerador também aceita `--sem-jev` (o teste local compara com esse fluxo, porque a demo já tem a credencial).

Pedido do PM Técnico em 25/11: não mexer em `gerar_fluxos.py` até o Pacote E ser commitado. O passo do Jev está pronto em `jev_sombra.py`; para ligar, colar este bloco em `gerar_fluxos.py` logo antes da linha `SAIDA = PASTA / "gerados" / SLUG` e trocar essa linha pela última abaixo:

```python
# Jev em modo sombra (25/11, PLANO-JEV-SOMBRA.md): só entra se a clínica tiver a credencial "typesafe" em credenciais_n8n.
# "--jev-teste" gera uma cópia com credencial falsa em gerados/<slug>-jev-teste/, só para o teste local (teste_jev_sombra.js).
JEV_TESTE = "--jev-teste" in sys.argv[2:]
if JEV_TESTE:
    CRED["typesafe"] = {"httpHeaderAuth": {"id": "TESTE-SEM-CHAVE", "name": "TypeSafe (teste local)"}}
if "typesafe" in CRED:
    import jev_sombra
    jev_sombra.adicionar(A, code, http, pg, se, cond, COMUM_JS)

SAIDA = PASTA / "gerados" / (SLUG + ("-jev-teste" if JEV_TESTE else ""))
```

Depois: `python gerar_fluxos.py clinica-demo && python gerar_fluxos.py clinica-demo --jev-teste && node teste_jev_sombra.js` (40 de 40 em 25/11, com o bloco colado; `--real` faz 2 chamadas de verdade, 42 de 42).

## O que precisa de OK da Erica

- Criar a tabela no banco da demo e da clínica de teste.
- Criar a credencial "TypeSafe" no n8n e pôr a chave no `/opt/keshion/.env`.
- Publicar o fluxo (import e publish, sem reiniciar o n8n).
