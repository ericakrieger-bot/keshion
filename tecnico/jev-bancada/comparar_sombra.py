# -*- coding: utf-8 -*-
"""Comparação "Jev x regra de hoje" com os dados do modo sombra (tabela jev_sombra; plano em tecnico/n8n/PLANO-JEV-SOMBRA.md).
Só LÊ o banco no servidor (um SELECT), não muda nada. Rodar depois de 1 a 2 semanas de dados.
Uso (dentro de tecnico/jev-bancada):
    python comparar_sombra.py                 # banco clara (demo), últimos 14 dias
    python comparar_sombra.py clara 7         # banco e número de dias
    python comparar_sombra.py --arquivo x.json  # lê uma exportação salva (lista de linhas da tabela), sem servidor
A senha do banco fica no /opt/keshion/.env do servidor e nunca passa por aqui. Telefone aparece só com os 4 últimos dígitos.
"""
import json, os, re, subprocess, sys

SSH = ['ssh', '-i', os.path.expanduser('~/.ssh/keshion_vps'), 'root@169.58.41.107']


def ler_servidor(banco, dias):
    if not re.fullmatch(r'[a-z_]+', banco) or not (1 <= dias <= 60):
        sys.exit('banco só com letras minúsculas e _; dias de 1 a 60')
    q = f"SELECT coalesce(json_agg(j ORDER BY criado_em), '[]') FROM jev_sombra j WHERE criado_em > now() - interval '{dias} days'"
    cmd = ("cd /opt/keshion; set -a; . ./.env; set +a; docker compose exec -T postgres sh -c "
           f"'PGPASSWORD=\"$CLARA_DB_PASSWORD\" psql -v ON_ERROR_STOP=1 -h localhost -U clara -d {banco} -At'")
    r = subprocess.run(SSH + [cmd], input=q, capture_output=True, text=True, encoding='utf8')
    if r.returncode:
        sys.exit('erro ao ler o banco: ' + r.stderr.strip()[:300])
    return json.loads(r.stdout.strip() or '[]')


def tel(t):
    return '...' + str(t or '')[-4:]


def curta(m, n=90):
    return str(m or '').replace('\n', ' ')[:n]


def comparar(linhas):
    print(f'{len(linhas)} respostas da assistente no período\n')
    if not linhas:
        return
    ok = [x for x in linhas if x.get('ok')]
    falhas = [x for x in linhas if not x.get('ok')]
    ms = sorted(x['ms'] for x in linhas if x.get('ms') is not None)
    custo = sum(float(x.get('custo_usd') or 0) for x in ok)
    print('## Saúde do Jev')
    print(f'  ok: {len(ok)}; falhas: {len(falhas)} ({100 * len(falhas) / len(linhas):.1f}%)')
    if ms:
        print(f'  tempo: mediana {ms[len(ms) // 2]} ms; 95% abaixo de {ms[int(len(ms) * .95)]} ms; máximo {ms[-1]} ms')
    print(f'  custo total: US$ {custo:.4f}')
    motivos = {}
    for x in falhas:
        k = re.sub(r'\d+', 'N', str(x.get('erro') or 'sem motivo'))[:60]
        motivos[k] = motivos.get(k, 0) + 1
    for k, v in sorted(motivos.items(), key=lambda kv: -kv[1]):
        print(f'    {v}x {k}')

    print('\n## 1. Urgência (Jev avisa com 0,3 ou mais)')
    so_jev = [x for x in ok if x['decide_urgencia'] and not x['regra_urgencia']]
    so_regra = [x for x in ok if x['regra_urgencia'] and not x['decide_urgencia']]
    print(f'  os dois avisariam: {len([x for x in ok if x["decide_urgencia"] and x["regra_urgencia"]])}')
    print(f'  só o Jev avisaria: {len(so_jev)}  (conferir: urgência que a regra perdeu ou alarme falso do Jev?)')
    for x in so_jev:
        print(f'    {x["criado_em"][:16]} {tel(x["telefone"])} p={x["jev_urgencia"]:.2f} {curta(x["mensagem"])!r}')
    print(f'  só a regra avisaria: {len(so_regra)}  (o Jev nunca tira urgência: com o OU, esses continuam avisando)')
    for x in so_regra:
        print(f'    {x["criado_em"][:16]} {tel(x["telefone"])} p={x["jev_urgencia"]:.2f} {curta(x["mensagem"])!r}')

    print('\n## 2. "Dói?" e fora da lista')
    perg = [x for x in ok if x['decide_dor'] == 'pergunta']
    print(f'  "dói?" lido como pergunta (não relato): {len(perg)}; destes, a regra mandou para a equipe por urgência: '
          f'{len([x for x in perg if x["regra_urgencia"]])}')
    for x in perg:
        print(f'    p={x["jev_dor_p"]:.2f} regra={x["regra_rota"]} {curta(x["mensagem"])!r}')
    fora = [x for x in ok if x['decide_fora'] != 'nao']
    print(f'  fora da lista (implante, dentadura, coroa sobre implante): {len(fora)}')
    for x in fora:
        print(f'    {x["decide_fora"]} p={x["jev_fora"]:.2f} regra={x["regra_rota"]}/{x["regra_acao"]} {curta(x["mensagem"])!r}')

    print('\n## 3. Cancelar (só quando a assistente tinha perguntado de cancelar)')
    canc = [x for x in ok if x.get('perguntou_cancelar')]
    print(f'  {len(canc)} respostas à pergunta de cancelar')
    for rotulo, cond in (('regra cancelou e o Jev também', lambda x: x['regra_cancelou'] and x['decide_cancelar'] == 'cancela'),
                         ('regra NÃO cancelou e o Jev cancelaria (loop que o Jev evitaria?)', lambda x: not x['regra_cancelou'] and x['decide_cancelar'] == 'cancela'),
                         ('regra cancelou e o Jev perguntaria de novo (cancelamento indevido?)', lambda x: x['regra_cancelou'] and x['decide_cancelar'] != 'cancela'),
                         ('nenhum dos dois cancelou', lambda x: not x['regra_cancelou'] and x['decide_cancelar'] != 'cancela')):
        g = [x for x in canc if cond(x)]
        print(f'  {rotulo}: {len(g)}')
        if 'e o Jev' in rotulo or 'NÃO' in rotulo:
            for x in g:
                print(f'    sim={x["jev_conf_sim"]:.2f} espera={x["jev_espera"]:.2f} pede={x["jev_pede_cancelar"]:.2f} {curta(x["mensagem"])!r}')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--arquivo']:
        comparar(json.load(open(a[1], encoding='utf8')))
    else:
        comparar(ler_servidor(a[0] if a else 'clara', int(a[1]) if len(a) > 1 else 14))
