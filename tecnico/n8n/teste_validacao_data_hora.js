// Teste local (sem servidor, sem WhatsApp, sem custo) da conferência "o dia e a hora apareceram na conversa?"
// que o fluxo faz antes de marcar. Lê o código do nó "Validar o pedido de agenda" do fluxo gerado e roda vários casos.
// Uso (dentro de tecnico/n8n):  python gerar_fluxos.py clinica-demo   e depois   node teste_validacao_data_hora.js [clinica-demo]
const fs = require('fs');
const slug = process.argv[2] || 'clinica-demo';
const fluxo = JSON.parse(fs.readFileSync(__dirname + '/gerados/' + slug + '/atendimento.json', 'utf8'));
const no = fluxo.nodes.find(n => n.name === 'Validar o pedido de agenda');
const js = no.parameters.jsCode;
const ini = js.indexOf('const dd = String(');
const fim = js.indexOf('if (!temData || !temHora)');
if (ini < 0 || fim < 0) { console.error('Trecho não encontrado no fluxo gerado.'); process.exit(2); }
const trecho = js.slice(ini, fim);
const confere = new Function('conversa', 'q', trecho + '; return { temData, temHora };');

// [conversa, dia, mês, hora (0 a 23), data deve valer?, hora deve valer?, descrição]
const C = [
  // Português (tem de continuar funcionando)
  ['Clara: Tenho quinta, 19/11, às 11h.', 19, 11, 11, 1, 1, 'pt: 19/11 às 11h'],
  ['Paciente: pode ser dia 19 às 9:00', 19, 11, 9, 1, 1, 'pt: dia 19 às 9:00'],
  ['Paciente: pode ser dia 05 às 14h', 5, 11, 14, 1, 1, 'pt: dia 05 (zero)'],
  ['Clara: terça 3/12 às 15h', 3, 12, 15, 1, 1, 'pt: 3/12'],
  ['Paciente: quero 19 de novembro às 11h', 19, 11, 11, 1, 1, 'pt: 19 de novembro'],
  ['Paciente: 1º de dezembro às 9h', 1, 12, 9, 1, 1, 'pt: 1º de dezembro'],
  ['Paciente: quinta, 19 nov, às 11h', 19, 11, 11, 1, 1, 'pt: 19 nov'],
  ['Paciente: quinta 19 às 11h', 19, 11, 11, 1, 1, 'pt: quinta 19'],
  ['Paciente: quinta-feira 19 às 11h', 19, 11, 11, 1, 1, 'pt: quinta-feira 19'],
  ['Paciente: 19/11/2026 às 16h', 19, 11, 16, 1, 1, 'pt: 19/11/2026'],
  ['Paciente: 19 / 11 às 16h', 19, 11, 16, 1, 1, 'pt: 19 / 11 com espaços'],
  // Inglês
  ['Clara: I have Thursday, Nov 19, at 11am', 19, 11, 11, 1, 1, 'en: Thursday, Nov 19, at 11am'],
  ['Paciente: Thursday, Nov 19 at 11am works for me', 19, 11, 11, 1, 1, 'en: Thursday, Nov 19 at 11am'],
  ['Paciente: November 19 at 11 am', 19, 11, 11, 1, 1, 'en: November 19 at 11 am'],
  ['Paciente: November 19th at 11:00 a.m.', 19, 11, 11, 1, 1, 'en: November 19th, 11:00 a.m.'],
  ['Paciente: Nov. 19th, 11am', 19, 11, 11, 1, 1, 'en: Nov. 19th'],
  ['Paciente: 19 Nov at 11am', 19, 11, 11, 1, 1, 'en: 19 Nov'],
  ['Paciente: 19th of November at 11am', 19, 11, 11, 1, 1, 'en: 19th of November'],
  ['Paciente: the 19th at 11am', 19, 11, 11, 1, 1, 'en: the 19th'],
  ['Paciente: on the 19th, 11am', 19, 11, 11, 1, 1, 'en: on the 19th'],
  ['Paciente: 19th works, 11am', 19, 11, 11, 1, 1, 'en: 19th'],
  ['Paciente: Thursday 19 at 11am', 19, 11, 11, 1, 1, 'en: Thursday 19'],
  ['Paciente: Tuesday, Nov 24 at 9am would be good', 24, 11, 9, 1, 1, 'en: Tuesday, Nov 24 at 9am (Emily)'],
  ['Paciente: Thursday, Nov 26 at 2pm', 26, 11, 14, 1, 1, 'en: Nov 26 at 2pm'],
  ['Paciente: Dec 1st at 9 am', 1, 12, 9, 1, 1, 'en: Dec 1st'],
  ['Paciente: December 3 at 4:00 p.m.', 3, 12, 16, 1, 1, 'en: December 3 at 4:00 p.m.'],
  ['Paciente: Nov 05 at 4 pm', 5, 11, 16, 1, 1, 'en: Nov 05 (zero)'],
  ['Paciente: 11/19 at 11am', 19, 11, 11, 1, 1, 'en: 11/19 (formato dos EUA)'],
  ['Paciente: 2026-11-19 at 11am', 19, 11, 11, 1, 1, 'iso: 2026-11-19'],
  // Espanhol
  ['Paciente: el 19 de noviembre a las 11', 19, 11, 11, 1, 1, 'es: 19 de noviembre a las 11'],
  ['Paciente: el jueves 19 a las 11', 19, 11, 11, 1, 1, 'es: jueves 19'],
  ['Paciente: el día 19 a las 11', 19, 11, 11, 1, 1, 'es: el día 19'],
  ['Paciente: el 19 a las 11', 19, 11, 11, 1, 1, 'es: el 19'],
  ['Paciente: 1 de diciembre a las 9', 1, 12, 9, 1, 1, 'es: 1 de diciembre'],
  // Não pode aceitar dia errado
  ['Paciente: são 11:19 agora', 19, 11, 11, 0, 1, 'NÃO: 11:19 (hora)'],
  ['Paciente: custa R$ 1.019 e pago em 3 vezes', 19, 11, 11, 0, 0, 'NÃO: R$ 1.019'],
  ['Paciente: preciso às 19h', 19, 11, 19, 0, 1, 'NÃO: 19h (hora)'],
  ['Paciente: Thursday 11am works', 11, 11, 11, 0, 1, 'NÃO: Thursday 11am (hora, dia 11)'],
  ['Paciente: Thursday at 11 am', 11, 11, 11, 0, 1, 'NÃO: Thursday at 11 am'],
  ['Paciente: quinta 19h', 19, 11, 19, 0, 1, 'NÃO: quinta 19h'],
  ['Paciente: Nov 20 at 11am', 19, 11, 11, 0, 1, 'NÃO: Nov 20 quando o dia é 19'],
  ['Paciente: Nov 2026', 20, 11, 11, 0, 0, 'NÃO: Nov 2026 (ano)'],
  ['Paciente: Nov 1 at 11am', 19, 11, 11, 0, 1, 'NÃO: Nov 1 quando o dia é 19'],
  ['Paciente: Nov 19 at 11am', 1, 11, 11, 0, 1, 'NÃO: Nov 19 quando o dia é 1'],
  ['Paciente: 19 Dec at 11am', 19, 11, 11, 0, 1, 'NÃO: 19 Dec quando o mês é novembro'],
  ['Paciente: December 19 at 11am', 19, 11, 11, 0, 1, 'NÃO: December 19 quando o mês é novembro'],
  ['Paciente: 19 de dezembro às 11h', 19, 11, 11, 0, 1, 'NÃO: 19 de dezembro quando o mês é novembro'],
  ['Paciente: 29/11 às 11h', 19, 11, 11, 0, 1, 'NÃO: 29/11 quando o dia é 19'],
  ['Paciente: 19/12 às 11h', 19, 11, 11, 0, 1, 'NÃO: 19/12 quando o mês é novembro'],
  ['Paciente: 3/19 às 11h', 19, 11, 11, 0, 1, 'NÃO: 3/19 (março, dia 19)'],
  ['Paciente: the 20th at 11am', 19, 11, 11, 0, 1, 'NÃO: the 20th quando o dia é 19'],
  ['Paciente: the 119th row', 19, 11, 11, 0, 0, 'NÃO: 119th'],
  ['Paciente: 2019 foi o ano', 19, 11, 11, 0, 0, 'NÃO: 2019'],
  ['Paciente: 11/12 às 9h', 11, 11, 9, 0, 1, 'NÃO: 11/12 quando o mês é novembro (dia 11)'],
  ['Paciente: lembro de mar 19 do ano passado', 19, 11, 11, 0, 0, 'NÃO: mar 19 (março) quando o mês é novembro'],
  // Hora (continua funcionando e não aceita hora errada)
  ['Paciente: às 9', 19, 11, 9, 0, 1, 'hora: às 9'],
  ['Paciente: 4 pm', 19, 11, 16, 0, 1, 'hora: 4 pm'],
  ['Paciente: at 4', 19, 11, 16, 0, 1, 'hora: at 4'],
  ['Paciente: a las 9', 19, 11, 9, 0, 1, 'hora: a las 9'],
  ['Paciente: at 4:30', 19, 11, 16, 0, 0, 'hora: 4:30 não vale como 4'],
  ['Paciente: 10am', 19, 11, 11, 0, 0, 'hora: 10am não vale como 11'],
];

const fmt = (dia, mes, hora) => ({ day: String(dia).padStart(2, '0'), month: String(mes).padStart(2, '0'), hour: String(hora).padStart(2, '0') });
let falhas = 0;
for (const [conv, dia, mes, hora, dataOk, horaOk, desc] of C) {
  const r = confere(conv, fmt(dia, mes, hora));
  const ok = r.temData === !!dataOk && r.temHora === !!horaOk;
  if (!ok) { falhas++; console.log('FALHOU  ' + desc + '  (data ' + r.temData + ' esperada ' + !!dataOk + '; hora ' + r.temHora + ' esperada ' + !!horaOk + ')'); }
}
console.log((C.length - falhas) + ' de ' + C.length + ' casos certos' + (falhas ? ', ' + falhas + ' falharam' : '') + ' (' + slug + ')');
process.exit(falhas ? 1 : 0);
