const fs=require('fs');
const w=JSON.parse(fs.readFileSync(0,'utf8'));
const js=w.nodes.find(n=>n.name==='Validar o pedido de agenda').parameters.jsCode;
const start=js.indexOf('const dd = String('),end=js.indexOf('if (!temData || !temHora)');
const detect=new Function('conversa','q',js.slice(start,end)+';return {temData,temHora};');
const cases=[
 ['Paciente: 19/11 às 9:30',19,11,9,false,'minutos diferentes'],
 ['Paciente: 19/11 às 14:59',19,11,14,false,'minutos diferentes à tarde'],
 ['Paciente: 19/11/2025 às 9h',19,11,9,false,'ano passado'],
 ['Paciente: 2027-11-19 às 9h',19,11,9,false,'ano seguinte'],
 ['Paciente: dia 19 de dezembro às 9h',19,11,9,false,'mês explícito diferente após dia'],
 ['Paciente: the 19th of December at 9am',19,11,9,false,'ordinal com mês diferente'],
 ['Paciente: Thursday 19 December at 9am',19,11,9,false,'semana com mês diferente'],
 ['Paciente: my 19th installment is R$ 200. I wake up at 9am.',19,11,9,false,'ordinal não é data'],
 ['Paciente: meu CEP é 81911-190 às 9h',19,11,9,false,'CEP'],
 ['Paciente: meu telefone é 554199900919 e quero 9am',19,11,9,false,'telefone'],
 ['Paciente: custa R$ 1.019,00 às 9h',19,11,9,false,'reais decimal'],
 ['Paciente: custa R$ 19/11 parcelas às 9h',19,11,9,false,'fração de valor não é data'],
 ['Paciente: nasci em 2019, às 9h',19,11,9,false,'ano isolado'],
 ['Paciente: Thursday 11am',11,11,11,false,'dia confundido com hora'],
 ['Paciente: dia 19h; prefiro 9am',19,11,9,false,'dia seguido de hora'],
 ['Paciente: 19.11 às 9h',19,11,9,true,'data com ponto'],
 ['Paciente: 19-11 às 9h',19,11,9,true,'data com hífen'],
 ['Paciente: 19 de noviembre a las nueve',19,11,9,true,'hora por extenso espanhol'],
 ['Paciente: November nineteenth at nine am',19,11,9,true,'data e hora por extenso inglês'],
 ['Paciente: 19 de novembro às nove',19,11,9,true,'hora por extenso português'],
 ['Paciente: amanhã às 9h',19,11,9,true,'relativa amanhã com relógio em 18/11'],
 ['Paciente: tomorrow at 9am',19,11,9,true,'relativa tomorrow'],
 ['Paciente: next Friday at 9am',20,11,9,true,'detecção de relativa next Friday; regra de sexta é separada'],
 ['Paciente: daqui a 3 dias às 9h',21,11,9,true,'detecção de relativa em três dias; regra de sábado é separada'],
 ['Paciente: 1/12 at 9am',1,12,9,true,'dia mês brasileiro'],
 ['Paciente: 12/1 at 9am',1,12,9,true,'mês dia americano ambíguo'],
 ['Paciente: Nov 19 at 9am',19,11,9,true,'controle inglês'],
 ['Paciente: 19 de noviembre a las 9',19,11,9,true,'controle espanhol'],
 ['Paciente: 19/11 às 9h',19,11,9,true,'controle português'],
 ['Paciente: Nov 19 at 9pm',19,11,9,false,'AM PM errado'],
 ['Clara: 19/11 às 9h ou 24/11 às 16h?\nPaciente: Quero 24/11 às 16h.',19,11,16,false,'data de uma oferta e hora da outra'],
 ['Clara: 19/11 às 9h?\nPaciente: Não quero esse horário.',19,11,9,false,'recusa explícita'],
 ['Paciente: Pode ser 19/11 às 9h.\nPaciente: Corrigindo, quero 24/11 às 16h.',19,11,9,false,'escolha antiga corrigida'],
];
let out=cases.map(([text,day,month,hour,expected,why])=>{
 const result=detect(text,{day:String(day).padStart(2,'0'),month:String(month).padStart(2,'0'),hour:String(hour).padStart(2,'0')});
 const accepted=result.temData&&result.temHora;
 return {text,day,month,hour,expected,accepted,why,...result,ok:accepted===expected};
});
// Conferir o nó inteiro, não só o detector de texto.
class TestDate extends Date{constructor(...args){super(...(args.length?args:['2026-11-18T12:00:00Z']))} static now(){return new Date('2026-11-18T12:00:00Z').getTime()}}
function full(text,iso){
 const refs={'Decidir a ação':{acao:'agendar',inicio:iso,nome_completo:'Teste Codex',telefone_contato:'554199900954'},'Ler ficha e instruções (só a última responde)':{conversa:text,pendente:''}};
 return new Function('$','Date',js)(n=>({first:()=>({json:refs[n]})}),TestDate)[0].json;
}
const fullCases=[
 {text:'Paciente: 19/11 às 9:30',iso:'2026-11-19T09:00:00-03:00'},
 {text:'Paciente: dia 19 de dezembro às 9h',iso:'2026-11-19T09:00:00-03:00'},
 {text:'Clara: 19/11 às 9h ou 24/11 às 16h?\nPaciente: Quero 24/11 às 16h.',iso:'2026-11-19T16:00:00-03:00'},
 {text:'Paciente: 19/11 às 9h',iso:'2026-11-19T09:00:59-03:00'},
 {text:'Paciente: amanhã às 9h',iso:'2026-11-19T09:00:00-03:00'},
].map(c=>({...c,result:full(c.text,c.iso)}));
console.log(JSON.stringify({total:out.length,corretos:out.filter(x=>x.ok).length,divergencias:out.filter(x=>!x.ok).length,casos:out,noCompleto:fullCases},null,2));
