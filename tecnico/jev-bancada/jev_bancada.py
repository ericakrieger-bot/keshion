# -*- coding: utf-8 -*-
"""Bancada do Jev (TypeSafe) como segunda barreira da Clara.
Só roda no PC. Não toca em n8n, servidor, banco nem WhatsApp. Só conversas inventadas.
Uso (dentro de tecnico/jev-bancada):
    python jev_bancada.py rodar      # chama o Jev e guarda tudo em jev_resultados.json
    python jev_bancada.py analisar   # lê jev_resultados.json e gera a tabela (sem custo)
A chave TYPESAFE_API_KEY é lida do .env da raiz do projeto, só dentro do script. Nunca é impressa nem gravada.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
ARQ_CONVERSAS = os.path.join(RAIZ, 'tecnico', 'teste-ab', 'paciente-simulado-20261124-214610.json')
ARQ_RES = os.path.join(AQUI, 'jev_resultados.json')
MODELO = 'jev-latest'
PRECO_ENTRADA_POR_MILHAO = 0.042  # US$, Jev 1.14; saída grátis
LIMITE_AVISO = 1.00   # US$: para e avisa
LIMITE_TOTAL = 3.00

# ---------------------------------------------------------------- perguntas
NOUL_URG = {
    'type': 'noul',
    'instructions': 'Na `mensagem_do_paciente`, o paciente relata que AGORA está com dificuldade para respirar, '
                    'dificuldade para engolir, sangramento, inchaço no rosto ou na boca com febre, ou dor muito forte?',
    'criteria': {
        'true': 'O paciente diz que está sentindo isso neste momento (por exemplo: "estou sangrando", '
                '"não consigo engolir", "meu rosto está inchado e estou com febre", "a dor está insuportável").',
        'false': 'O paciente só pergunta se algo é comum ou se um procedimento causa isso, fala de algo que passou, '
                 'diz que NÃO tem o sintoma, ou trata de outro assunto (preço, horário, cancelar).'}}

CHOICE_DOR = {
    'type': 'choice',
    'instructions': 'A `mensagem_do_paciente` relata uma dor que o paciente sente agora, ou pergunta se um procedimento dói?',
    'criteria': {
        'relato_de_dor': 'O paciente diz que está com dor ou sensibilidade agora ou há pouco ("estou com dor", "está doendo", "não consigo comer de tanta dor").',
        'pergunta_sobre_o_procedimento': 'O paciente pergunta se um tratamento ou procedimento dói ou incomoda, sem dizer que sente dor agora ("dói?", "a limpeza dói?", "e se ela falar que dói muito?").',
        'outro': 'A mensagem não fala de dor.'}}

CHOICE_CONF = {
    'type': 'choice',
    'instructions': 'Considerando `ultima_fala_da_clara`, a `mensagem_do_paciente` responde com um sim claro, um não, uma dúvida ou fala de outro assunto?',
    'criteria': {
        'sim_claro': 'O paciente concorda de forma direta com o que a Clara perguntou ("sim", "isso mesmo", "pode cancelar", "sim, pode cancelar, mas antes me responde X"). Perguntas extras do paciente não tiram o sim, desde que ele confirme o que foi perguntado.',
        'nao': 'O paciente recusa ou corrige o que a Clara perguntou ("não", "quero manter", "não é a minha, é da minha filha").',
        'duvida': 'O paciente não decide: está inseguro, pede para esperar ou responde com outra pergunta no lugar da resposta ("sim?", "não sei", "espera").',
        'outro_assunto': 'O paciente não responde ao que a Clara perguntou e fala de outra coisa (preço, endereço, sintoma).'}}

CHOICE_HOR = {
    'type': 'choice',
    'instructions': 'Considerando os horários que a Clara ofereceu em `ultima_fala_da_clara`, o paciente escolheu um deles, está só vendo, ou recusou?',
    'criteria': {
        'escolheu_horario_oferecido': 'O paciente aceita um dos horários oferecidos de forma clara (cita o dia e a hora, ou diz "esse", "o primeiro").',
        'so_vendo': 'O paciente ainda não escolheu: faz perguntas, pede outras opções ou diz que vai ver.',
        'recusou': 'O paciente diz que nenhum horário serve ou desiste de marcar.'}}

NOUL_FORA = {
    'type': 'noul',
    'instructions': 'A `mensagem_do_paciente` pede ou pergunta sobre algo que a clínica não faz: implante, dentadura ou prótese removível, ou coroa sobre implante?',
    'criteria': {
        'true': 'O paciente quer saber preço, prazo ou se fazem implante, dentadura/prótese total ou coroa sobre implante.',
        'false': 'O paciente fala de outro assunto (limpeza, clareamento, lentes, alinhador, restauração, canal, extração, preço de outro serviço, horário).'}}

NOUL_REMARCAR = {
    'type': 'noul',
    'instructions': 'O paciente pede para remarcar ou marcar de novo uma avaliação ou consulta que perdeu ou desmarcou?',
    'criteria': {
        'true': 'O paciente diz que faltou ou desmarcou e quer outro horário.',
        'false': 'O paciente não pede um novo horário.'}}

PERGUNTAS = {'urg': NOUL_URG, 'dor': CHOICE_DOR, 'conf': CHOICE_CONF, 'hor': CHOICE_HOR, 'fora': NOUL_FORA, 'remarcar': NOUL_REMARCAR}


def chave():
    for l in open(os.path.join(RAIZ, '.env'), encoding='utf8'):
        if l.startswith('TYPESAFE_API_KEY='):
            return l.split('=', 1)[1].strip().strip('"\'')
    sys.exit('TYPESAFE_API_KEY não está no .env')


def montar_state(hist, msg):
    """hist: lista de (quem, texto) anteriores à mensagem; pega as últimas 6 trocas (12 falas)."""
    ult = hist[-12:]
    clara = [t for q, t in hist if q.startswith('C')]
    return {
        'conversa_recente': [{'quem': 'Clara (atendente virtual da clínica)' if q.startswith('C') else 'Paciente', 'texto': t} for q, t in ult],
        'ultima_fala_da_clara': clara[-1] if clara else '(a Clara ainda não falou)',
        'mensagem_do_paciente': msg}


def chamar(k, state, perguntas=None):
    corpo = json.dumps({'model': MODELO, 'state': state, 'questions': perguntas or PERGUNTAS}).encode()
    for tent in range(4):
        req = urllib.request.Request('https://api.typesafe.ai/v1/systemone', data=corpo,
                                     headers={'Authorization': 'Bearer ' + k, 'Content-Type': 'application/json'})
        t0 = time.time()
        try:
            r = json.load(urllib.request.urlopen(req, timeout=90))
            return {'ok': True, 'seg': round(time.time() - t0, 3), 'resp': r}
        except urllib.error.HTTPError as e:
            txt = e.read().decode('utf8', 'replace')[:300]
            if e.code in (429, 500, 502, 503) and tent < 3:
                time.sleep(2 * (tent + 1)); continue
            return {'ok': False, 'seg': round(time.time() - t0, 3), 'erro': f'HTTP {e.code}: {txt}'}
        except Exception as e:
            if tent < 3: time.sleep(2); continue
            return {'ok': False, 'seg': round(time.time() - t0, 3), 'erro': str(e)[:200]}


# ---------------------------------------------------------------- casos
def casos_conversas():
    d = json.load(open(ARQ_CONVERSAS, encoding='utf8'))
    out = []
    for i, x in enumerate(d):
        nome = x['paciente'].split(' (')[0]
        conv = x['conversa']
        for j, (q, t) in enumerate(conv):
            if q.startswith('P'):
                out.append({'id': f'conv{i:02d}-{j:02d}', 'grupo': 'conversa', 'quem': nome, 'hist': conv[:j], 'msg': t})
    return out


PERG_CANC = 'Só para confirmar: você quer cancelar a sua avaliação de 19/11 às 11:00, certo?'


def casos_sinteticos():
    """Casos de teste_pacote_c.js e testes-codex/ (copiados à mão) + alguns inventados para urgência e fora da lista."""
    out = []
    def add(grupo, msg, hist=None, **gold):
        out.append({'id': f'{grupo}-{len([o for o in out if o["grupo"] == grupo]) + 1:02d}', 'grupo': grupo, 'quem': grupo, 'hist': hist or [], 'msg': msg, 'gold': gold})
    # urgência (C3 do Pacote C + Codex + 2 inventados que a lista de palavras não pega)
    for m in ['estou sangrando, o que faço?', 'minha gengiva está sangrando muito, é normal?', 'I am bleeding, what should I do?',
              'mi cara está hinchada, ¿qué hago?', 'tengo mucho dolor, ¿qué puedo hacer?', 'estou com febre e dor forte',
              'tô com o rosto inchado, quero cancelar', 'minha gengiva está sangrando muito', 'não estou com febre mas estou sangrando',
              'Agora estou sangrando', 'não consigo engolir direito, parece que a garganta está fechando',
              'depois da anestesia estou com dificuldade de respirar', 'meu rosto inchou muito e estou com febre desde ontem']:
        add('urgencia', m, urg=True)
    for m in ['não estou com febre', 'não tenho dor forte nem inchaço', 'sem febre e sem sangramento', 'no tengo fiebre',
              'no he tenido hinchazón', "I don't have a fever", 'I do not have any swelling', 'clareamento faz a gengiva sangrar?',
              'depois do implante é normal sangrar?', 'quero marcar uma avaliação', 'quanto custa a limpeza?']:
        add('urgencia', m, urg=False)
    # dor x pergunta (inventados, no estilo da Júlia)
    for m, g in [('dói?', 'pergunta_sobre_o_procedimento'), ('o clareamento dói?', 'pergunta_sobre_o_procedimento'),
                 ('e se ela falar que dói muito?', 'pergunta_sobre_o_procedimento'), ('a limpeza dói muito? tenho medo', 'pergunta_sobre_o_procedimento'),
                 ('estou com muita dor no dente desde ontem', 'relato_de_dor'), ('tá doendo muito, não consigo mastigar', 'relato_de_dor'),
                 ('meu dente está sensível e dói quando bebo água gelada', 'relato_de_dor'), ('quero marcar uma limpeza', 'outro')]:
        add('dor', m, dor=g)
    # fora da lista
    for m, g in [('quanto custa um implante?', True), ('vocês fazem dentadura?', True), ('quero colocar uma coroa em cima do implante', True),
                 ('preciso de uma dentadura nova, quanto fica?', True), ('vocês fazem limpeza?', False), ('quanto custa a lente?', False),
                 ('quero tirar o siso', False)]:
        add('fora', m, fora=g)
    # confirmação de cancelar (C1, C1b do Pacote C e Codex)
    h1 = [('Paciente', 'oi'), ('Clara', PERG_CANC)]
    SIM, NAO = ['sim_claro'], ['nao', 'duvida', 'outro_assunto']
    for m, ok in [('sim', SIM), ('Sim, pode cancelar por favor', SIM), ('isso mesmo', SIM),
                  ('isso é só uma dúvida, pode dizer o preço?', NAO), ('sim, mas quanto custa a limpeza?', ['duvida', 'outro_assunto', 'nao']),
                  ('sim. aliás, vocês atendem sábado', ['sim_claro', 'duvida', 'outro_assunto']),  # pode ser sim + pergunta
                  ('não, quero manter', NAO), ('sim, mas não cancela ainda', NAO), ('sim?', ['duvida', 'nao', 'outro_assunto'])]:
        add('cancelar', m, h1, conf=ok, cancela=(ok == SIM))
    h_en = [('Paciente', 'hi'), ('Clara', 'Just to confirm: you would like to cancel your evaluation on Thursday, Nov 19, at 11:00, correct?')]
    add('cancelar', 'Yes, please cancel it', h_en, conf=SIM, cancela=True)
    add('cancelar', "yes that's right", h_en, conf=SIM, cancela=True)
    h_es = [('Paciente', 'hola'), ('Clara', 'Solo para confirmar: ¿quieres cancelar tu evaluación del jueves 19 de noviembre a las 11:00, correcto?')]
    add('cancelar', 'Sí, cancélala', h_es, conf=SIM, cancela=True)
    h2 = lambda r1: [('Paciente', 'oi'), ('Clara', PERG_CANC), ('Paciente', r1), ('Clara', PERG_CANC)]
    add('cancelar', 'sim, pode cancelar esse horário mesmo', h2('sim, esse horário mesmo'), conf=SIM, cancela=True)
    add('cancelar', 'sim, claro, pode ser', h2('sim, obrigada'), conf=SIM, cancela=True)
    add('cancelar', 'sim, mas qual o endereço?', h2('sim, e o endereço?'), conf=['duvida', 'outro_assunto', 'nao'], cancela=False)
    add('cancelar', 'sim, mas não cancela ainda', h2('sim, esse horário mesmo'), conf=NAO, cancela=False)
    add('cancelar', 'não, quero manter', h2('sim, esse horário mesmo'), conf=NAO, cancela=False)
    # Codex
    add('cancelar', 'Não, quero manter.', [('Paciente', 'Quero cancelar.'), ('Clara', 'Posso cancelar sua avaliação?')], conf=NAO, cancela=False)
    add('cancelar', 'Please keep it.', [('Paciente', 'Quero cancelar.'), ('Clara', 'Your appointment can be canceled.')], conf=NAO, cancela=False)
    add('cancelar', 'Quero saber o preço.', [('Paciente', 'Quero cancelar.'), ('Clara', 'A sua avaliação é quinta, certo?')], conf=['duvida', 'outro_assunto', 'nao'], cancela=False)
    # escolha de horário
    OFERTA = [('Paciente', 'quero marcar uma avaliação'), ('Clara', 'Tenho quinta, 26/11, às 14h, terça, 01/12, às 9h, ou quinta, 03/12, às 14h. Qual fica melhor pra você?')]
    for m, g in [('quinta às 14h', 'escolheu_horario_oferecido'), ('pode ser o primeiro', 'escolheu_horario_oferecido'), ('o de terça 01/12 às 9h, por favor', 'escolheu_horario_oferecido'),
                 ('tem outro dia? esses não dão', 'so_vendo'), ('qual o endereço da clínica?', 'so_vendo'), ('sexta de manhã tem?', 'so_vendo'),
                 ('nenhum desses serve, vou ver e te aviso', 'recusou'), ('deixa pra lá, não quero mais marcar', 'recusou')]:
        add('horario', m, OFERTA, hor=g)
    return out


def rodar():
    k = chave()
    casos = casos_conversas() + casos_sinteticos()
    res = json.load(open(ARQ_RES, encoding='utf8')) if os.path.exists(ARQ_RES) else {}
    pend = [c for c in casos if c['id'] not in res or not res[c['id']]['chamada'].get('ok')]
    print(f'{len(casos)} casos, {len(pend)} para chamar')
    gasto = sum(r['chamada']['resp']['usage']['input_tokens'] for r in res.values() if r['chamada'].get('ok')) * PRECO_ENTRADA_POR_MILHAO / 1e6

    def uma(c):
        st = montar_state(c['hist'], c['msg'])
        return c, st, chamar(k, st)
    with ThreadPoolExecutor(4) as ex:
        for c, st, ch in ex.map(uma, pend):
            res[c['id']] = {'caso': c, 'state': st, 'chamada': ch}
            if ch['ok']:
                gasto += ch['resp']['usage']['input_tokens'] * PRECO_ENTRADA_POR_MILHAO / 1e6
            if gasto > LIMITE_AVISO:
                print('PAREI: gasto passou de US$ 1,00'); break
    json.dump(res, open(ARQ_RES, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    erros = [i for i, r in res.items() if not r['chamada'].get('ok')]
    print(f'gasto estimado até agora: US$ {gasto:.4f}; chamadas com erro: {len(erros)}')


# ---------------------------------------------------------------- análise (sem custo)
def ultima_frase(t):
    fr = re.split(r'(?<=[.!?])\s+', t.strip())
    return fr[-1] if fr else t


def gate_cancelar(c, lc):
    """Código decide: a última fala da Clara é uma pergunta de confirmar o cancelamento?"""
    if c['grupo'] == 'cancelar': return True
    f = ultima_frase(lc)
    return bool(re.search(r'cancel', f, re.I) and f.rstrip().endswith('?'))


def gate_horario(c, lc):
    if c['grupo'] == 'horario': return True
    return bool(re.search(r'\bou\b[^?]*\d{1,2}\s?h', lc) and '?' in ultima_frase(lc) and not re.search('cancel', lc, re.I))


SIM = ['sim_claro']; NAO3 = ['nao', 'duvida', 'outro_assunto']
# Rótulos feitos à mão (o que um atendente humano esperaria). Conversa sem rótulo: urgência=não e fora da lista=não.
GOLD = {
    **{f'conv00-{j:02d}': {'conf': SIM, 'cancela': True} for j in (16, 18, 20, 22, 24, 26)},
    'conv04-24': {'conf': SIM, 'cancela': True}, 'conv04-26': {'conf': SIM, 'cancela': True},
    'conv05-10': {'conf': SIM, 'cancela': True},
    **{f'conv05-{j:02d}': {'conf': NAO3, 'cancela': False} for j in (12, 14, 16, 18, 20, 24)},
    'conv08-12': {'conf': SIM, 'cancela': True}, 'conv08-14': {'conf': SIM, 'cancela': True},
    'conv13-16': {'conf': SIM, 'cancela': True},
    'conv14-14': {'conf': SIM, 'cancela': True}, 'conv14-16': {'conf': SIM, 'cancela': True},
    'conv19-08': {'conf': SIM, 'cancela': True}, 'conv19-10': {'conf': SIM, 'cancela': True},
    'conv00-08': {'hor': 'escolheu_horario_oferecido'}, 'conv05-06': {'hor': 'escolheu_horario_oferecido'},
    'conv08-04': {'hor': 'escolheu_horario_oferecido'}, 'conv19-02': {'hor': 'escolheu_horario_oferecido'},
    'conv04-02': {'hor': 'escolheu_horario_oferecido'}, 'conv14-06': {'hor': 'escolheu_horario_oferecido'},
    'conv13-06': {'hor': 'escolheu_horario_oferecido'},
    'conv08-00': {'dor': 'pergunta_sobre_o_procedimento'}, 'conv08-06': {'dor': 'pergunta_sobre_o_procedimento'},
    'conv00-14': {'dor': 'outro'},
    'conv02-00': {'urg': True, 'dor': 'relato_de_dor'}, 'conv02-02': {'urg': True, 'dor': 'relato_de_dor'},
    'conv02-10': {'urg': True, 'dor': 'relato_de_dor'},
    **{f'conv13-{j:02d}': {'urg': True, 'dor': 'relato_de_dor'} for j in (0, 2, 4, 6)},
    'conv07-06': {'fora': True}, 'conv07-08': {'fora': True},
    'conv21-00': {'remarcar': True}, 'conv21-02': {'remarcar': True},
}
# Turnos ambíguos, fora das contas: a dor continua na conversa, mas a mensagem não repete; ou a dúvida é de fato discutível.
AMBIGUOS_URG = {f'conv02-{j:02d}' for j in range(4, 28, 2)} | {f'conv13-{j:02d}' for j in range(8, 20, 2)}
AMBIGUOS_FORA = {'conv07-00', 'conv07-02', 'conv12-02', 'conv12-04', 'conv12-06'}


def gold_de(id_, c):
    g = dict(c.get('gold') or {})
    if c['grupo'] == 'conversa':
        g = dict(GOLD.get(id_, {}))
        if 'urg' not in g and id_ not in AMBIGUOS_URG: g['urg'] = False
        if 'fora' not in g and id_ not in AMBIGUOS_FORA: g['fora'] = False
    return g


def analisar():
    res = json.load(open(ARQ_RES, encoding='utf8'))
    ok = {i: r for i, r in res.items() if r['chamada'].get('ok')}
    linhas = []

    def R(*a): linhas.append(' '.join(str(x) for x in a))
    segs = sorted(r['chamada']['seg'] for r in ok.values())
    tin = [r['chamada']['resp']['usage']['input_tokens'] for r in ok.values()]
    tout = [r['chamada']['resp']['usage']['output_tokens'] for r in ok.values()]
    custo = sum(tin) * PRECO_ENTRADA_POR_MILHAO / 1e6
    R(f'chamadas: {len(res)} ok: {len(ok)} modelo: {sorted({r["chamada"]["resp"]["model"] for r in ok.values()})}')
    R(f'tempo por chamada (6 perguntas juntas): média {sum(segs)/len(segs):.2f}s, mediana {segs[len(segs)//2]:.2f}s, p95 {segs[int(len(segs)*.95)]:.2f}s, máx {segs[-1]:.2f}s')
    R(f'tokens de entrada por chamada: média {sum(tin)/len(tin):.0f} (mín {min(tin)}, máx {max(tin)}); saída média {sum(tout)/len(tout):.0f} (grátis)')
    R(f'custo total do que foi rodado: US$ {custo:.4f}; por mensagem (média): US$ {custo/len(ok):.6f}; por 1.000 mensagens: US$ {custo/len(ok)*1000:.3f}')
    dados = {k: [] for k in ('urg', 'fora', 'dor', 'conf', 'hor', 'remarcar')}
    for i, r in ok.items():
        c = r['caso']; a = r['chamada']['resp']['answers']; lc = r['state']['ultima_fala_da_clara']; g = gold_de(i, c)
        for q in ('urg', 'fora', 'remarcar'):
            if q in g: dados[q].append((i, c, g[q], a[q]['noul']))
        if 'dor' in g: dados['dor'].append((i, c, g['dor'], a['dor']))
        if 'conf' in g: dados['conf'].append((i, c, g, a['conf'], gate_cancelar(c, lc)))
        if 'hor' in g: dados['hor'].append((i, c, g['hor'], a['hor'], gate_horario(c, lc)))
    for q, nome in (('urg', 'URGÊNCIA'), ('fora', 'FORA DA LISTA'), ('remarcar', 'REMARCAR')):
        d = dados[q]; pos = [x for x in d if x[2]]; neg = [x for x in d if not x[2]]
        R(f'\n## {nome}: {len(pos)} casos que SIM, {len(neg)} que NÃO')
        for T in (0.3, 0.5, 0.67, 0.7, 0.9):
            fn = [x for x in pos if x[3] < T]; fp = [x for x in neg if x[3] >= T]
            R(f'  limiar {T}: perdeu {len(fn)} de {len(pos)} (falso negativo), alarme falso {len(fp)} de {len(neg)}')
        if pos and neg:
            R(f'  menor prob. entre os SIM: {min(x[3] for x in pos):.2f}; maior entre os NÃO: {max(x[3] for x in neg):.2f}')
        for x in pos:
            if x[3] < 0.67: R(f'    perdido(<0,67): {x[0]} p={x[3]:.2f} {x[1]["msg"][:80]!r}')
        for x in neg:
            if x[3] >= 0.3: R(f'    alarme(>=0,3): {x[0]} p={x[3]:.2f} {x[1]["msg"][:80]!r}')
    d = dados['dor']; certos = [x for x in d if x[3]['choice'] == x[2]]
    R(f'\n## DOR x PERGUNTA: {len(certos)} certos de {len(d)}')
    for x in d:
        if x[3]['choice'] != x[2]: R(f'    ERRO {x[0]} gold={x[2]} jev={x[3]["choice"]} {x[3]["probabilities"][x[3]["choice"]]:.2f} {x[1]["msg"][:70]!r}')
    d = [x for x in dados['conf'] if x[4]]
    R(f'\n## CONFIRMAÇÃO (só quando a Clara perguntou se cancela): {len(d)} casos; {len([x for x in dados["conf"] if not x[4]])} rotulados ficaram fora do filtro')
    pos = [x for x in d if x[2]['cancela']]; neg = [x for x in d if not x[2]['cancela']]
    ac = [x for x in d if x[3]['choice'] in x[2]['conf']]
    R(f'  acertos do rótulo: {len(ac)} de {len(d)}')
    for x in d:
        if x[3]['choice'] not in x[2]['conf']:
            R(f'    ERRO {x[0]} aceito={x[2]["conf"]} jev={x[3]["choice"]} {x[3]["probabilities"][x[3]["choice"]]:.2f} {x[1]["msg"][:70]!r}')
    R(f'  AÇÃO SEM VOLTA (cancelar só se P(sim_claro) >= limiar): {len(pos)} pedidos reais de cancelar, {len(neg)} que NÃO podem cancelar')
    for T in (0.5, 0.67, 0.8, 0.9, 0.93, 0.95, 0.97, 0.99):
        fc = [x for x in neg if x[3]['probabilities']['sim_claro'] >= T]; pe = [x for x in pos if x[3]['probabilities']['sim_claro'] < T]
        R(f'    limiar {T}: cancelou sem dever {len(fc)} de {len(neg)}; deixou de cancelar {len(pe)} de {len(pos)}')
    for x in neg:
        p = x[3]['probabilities']['sim_claro']
        if p >= 0.3: R(f'    NÃO deveria cancelar mas P(sim)={p:.2f}: {x[0]} {x[1]["msg"][:70]!r}')
    for x in pos:
        p = x[3]['probabilities']['sim_claro']
        if p < 0.93: R(f'    deveria cancelar mas P(sim)={p:.2f}: {x[0]} {x[1]["msg"][:70]!r}')
    sem = [(i, r) for i, r in ok.items() if r['caso']['grupo'] == 'conversa' and not gate_cancelar(r['caso'], r['state']['ultima_fala_da_clara'])]
    fa = [r['chamada']['resp']['answers']['conf']['probabilities']['sim_claro'] for _, r in sem]
    R(f'  SEM o filtro do código: em {len(sem)} falas em que a Clara NÃO perguntou de cancelar, P(sim_claro)>=0,67 em {len([p for p in fa if p >= .67])} e >=0,93 em {len([p for p in fa if p >= .93])}')
    d = [x for x in dados['hor'] if x[4]]
    R(f'\n## HORÁRIO (só quando a Clara ofereceu horários): {len(d)} casos; acertos {len([x for x in d if x[3]["choice"] == x[2]])}; {len([x for x in dados["hor"] if not x[4]])} rotulados fora do filtro')
    for x in d:
        if x[3]['choice'] != x[2]: R(f'    ERRO {x[0]} gold={x[2]} jev={x[3]["choice"]} {x[3]["probabilities"][x[3]["choice"]]:.2f} {x[1]["msg"][:70]!r}')
    R('\n## TABELA DE SITUAÇÕES')
    R('| caso | mensagem | pergunta | Jev disse | prob. | conf. | esperado | certo? |')
    R('|---|---|---|---|---|---|---|---|')

    def lin(i, q, esperado, certo, rotulo=''):
        r = res[i]; c = r['caso']; a = r['chamada']['resp']['answers'][q]
        msg = c['msg'].replace('\n', ' ').replace('|', '/')[:60]
        if a['type'] == 'noul': dis, pr, cf = ('sim' if a['noul'] >= .5 else 'não'), f"{a['noul']:.2f}", '-'
        else: dis, pr, cf = a['choice'], f"{a['probabilities'][a['choice']]:.2f}", f"{a['confidence']:.2f}"
        R(f"| {rotulo or c['quem']} ({i}) | {msg} | {q} | {dis} | {pr} | {cf} | {esperado} | {'sim' if certo(a) else 'NÃO'} |")
    ehsim = lambda a: a['choice'] == 'sim_claro'
    for j in (16, 18, 26): lin(f'conv00-{j:02d}', 'conf', 'sim_claro', ehsim, 'Bia')
    lin('conv00-14', 'dor', 'outro (pergunta sobre a lente)', lambda a: a['choice'] == 'outro', 'Bia')
    lin('conv05-10', 'conf', 'sim_claro', ehsim, 'Sandra')
    for j in (12, 14, 20, 24): lin(f'conv05-{j:02d}', 'conf', 'não sim (corrige: é da filha)', lambda a: a['choice'] != 'sim_claro', 'Sandra')
    lin('conv19-08', 'conf', 'sim_claro', ehsim, 'Thiago "Valeu!"')
    lin('conv19-10', 'conf', 'sim_claro', ehsim, 'Thiago')
    lin('conv19-12', 'conf', 'nao', lambda a: a['choice'] == 'nao', 'Thiago')
    lin('conv08-00', 'dor', 'pergunta_sobre_o_procedimento', lambda a: a['choice'] == 'pergunta_sobre_o_procedimento', 'Júlia "dói?"')
    lin('conv08-06', 'dor', 'pergunta_sobre_o_procedimento', lambda a: a['choice'] == 'pergunta_sobre_o_procedimento', 'Júlia')
    for j in (6, 8): lin(f'conv07-{j:02d}', 'fora', 'sim (implante/dentadura)', lambda a: a['noul'] >= .5, 'Dona Lourdes')
    for j in (0, 2): lin(f'conv21-{j:02d}', 'remarcar', 'sim (remarcar)', lambda a: a['noul'] >= .5, 'Diego')
    for k in range(1, 14): lin(f'urgencia-{k:02d}', 'urg', 'sim', lambda a: a['noul'] >= .5, f'Urgência #{k}')
    for k in range(14, 25): lin(f'urgencia-{k:02d}', 'urg', 'não', lambda a: a['noul'] < .5, f'Sem urgência #{k-13}')
    saida = '\n'.join(linhas)
    open(os.path.join(AQUI, 'analise.txt'), 'w', encoding='utf8').write(saida)
    print(saida)


# ---------------------------------------------------------------- experimento: cancelar com 3 perguntas separadas
ARQ_EXP = os.path.join(AQUI, 'jev_experimento_cancelar.json')
PERGUNTAS_CANCELAR = {
    'conf': CHOICE_CONF,
    'nao_ainda': {'type': 'noul',
                  'instructions': 'O paciente pede para esperar, para não cancelar ainda, ou quer manter a avaliação?',
                  'criteria': {'true': 'O paciente diz "não cancela ainda", "espera", "quero manter" ou deixa a decisão para depois.',
                               'false': 'O paciente não pede para esperar nem para manter.'}},
    'pede_cancelar': {'type': 'noul',
                      'instructions': 'O paciente pede de forma explícita para cancelar a avaliação (por exemplo "pode cancelar", "cancela")?',
                      'criteria': {'true': 'A mensagem diz com palavras próprias que quer cancelar ou manda cancelar.',
                                   'false': 'A mensagem só diz "sim" ou "isso" e depois fala de outro assunto, ou não pede para cancelar.'}}}


def cancelar2():
    k = chave()
    res = json.load(open(ARQ_RES, encoding='utf8'))
    alvo = [(i, r) for i, r in res.items() if r['chamada'].get('ok') and 'cancela' in gold_de(i, r['caso']) and gate_cancelar(r['caso'], r['state']['ultima_fala_da_clara'])]
    with ThreadPoolExecutor(4) as ex:
        saidas = list(ex.map(lambda ir: (ir[0], chamar(k, ir[1]['state'], PERGUNTAS_CANCELAR)), alvo))
    out = {i: {'state': res[i]['state'], 'chamada': ch} for i, ch in saidas}
    json.dump(out, open(ARQ_EXP, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    tok = sum(v['chamada']['resp']['usage']['input_tokens'] for v in out.values() if v['chamada'].get('ok'))
    print(f'{len(out)} chamadas; custo US$ {tok * PRECO_ENTRADA_POR_MILHAO / 1e6:.4f}')
    pos, neg = [], []
    for i, v in out.items():
        if not v['chamada'].get('ok'): print('erro', i); continue
        a = v['chamada']['resp']['answers']; c = res[i]['caso']
        reg = (a['conf']['probabilities']['sim_claro'], a['nao_ainda']['noul'], a['pede_cancelar']['noul'], c['msg'][:60].replace(chr(10), ' '), i)
        (pos if gold_de(i, c)['cancela'] else neg).append(reg)
    for T in (0.9, 0.93):
        for Tn in (0.3, 0.5):
            for Tp in (0.0, 0.5, 0.7):
                fc = [x for x in neg if x[0] >= T and x[1] < Tn and x[2] >= Tp]; pe = [x for x in pos if not (x[0] >= T and x[1] < Tn and x[2] >= Tp)]
                print(f'  P(sim)>={T}, P(nao_ainda)<{Tn}, P(pede_cancelar)>={Tp}: cancelou sem dever {len(fc)} de {len(neg)}; deixou de cancelar {len(pe)} de {len(pos)}')
    msgs = {i: res[i]['caso']['msg'] for i in out}
    r3 = lambda x: x[0] >= 0.93 and x[1] < 0.3 and ('?' not in msgs[x[4]] or x[2] >= 0.7)
    print(f'  REGRA MISTA (P(sim)>=0.93 e P(nao_ainda)<0.3 e (sem "?" na mensagem ou P(pede_cancelar)>=0.7)): cancelou sem dever {len([x for x in neg if r3(x)])} de {len(neg)}; deixou de cancelar {len([x for x in pos if not r3(x)])} de {len(pos)}')
    for x in neg:
        if r3(x): print('     cancelaria sem dever:', x[3], x[4])
    for x in pos:
        if not r3(x): print('     deixaria de cancelar:', x[3], x[4])
    print('NEGATIVOS (não podem cancelar): P(sim), P(nao_ainda), P(pede_cancelar)')
    for x in sorted(neg, key=lambda x: -x[0])[:8]: print('  ', [round(y, 2) if isinstance(y, float) else y for y in x])
    print('POSITIVOS: menores P(pede_cancelar)')
    for x in sorted(pos, key=lambda x: x[2])[:6]: print('  ', [round(y, 2) if isinstance(y, float) else y for y in x])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'rodar':
        rodar()
    elif len(sys.argv) > 1 and sys.argv[1] == 'cancelar2':
        cancelar2()
    elif len(sys.argv) > 1 and sys.argv[1] == 'analisar':
        analisar()
    else:
        print(__doc__)
