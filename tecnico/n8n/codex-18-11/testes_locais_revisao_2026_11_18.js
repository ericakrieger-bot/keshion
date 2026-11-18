const fs=require('fs');
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const nodes=Object.fromEntries(input.nodes.map(n=>[n.name,n]));
function run(name, data={}, refs={}) {
 const get=n=>({first:()=>({json:refs[n]||{}}),item:{json:refs[n]||{}},all:()=>refs[n]||[]});
 return new Function('$input','$',nodes[name].parameters.jsCode)({first:()=>({json:data}),all:()=>[{json:data}]},get);
}
const f={telefone:'554199900951',aprovador:'554199900952',pendente:'Agora estou sangrando',ultimo_aviso_humano:new Date().toISOString(),ultimo_motivo_humano:'dor de dente'};
let r=[];
let ia={acao:'humano',motivo:'sangramento novo',mensagem1:'Vou passar para a doutora.'};
let out=run('Resultado · humano',{}, {'Decidir a ação':ia,'Ler ficha e instruções (só a última responde)':f})[0].json;
r.push({teste:'novo sangramento curto depois de aviso',envios:JSON.parse(out.envios).length,aviso_humano:out.aviso_humano,texto:out.texto});
for (const [last,patient] of [['Posso cancelar sua avaliação?','Não, quero manter.'],['Your appointment can be canceled.','Please keep it.'],['A sua avaliação é quinta, certo?','Quero saber o preço.']]) {
 let refs={'Ler ficha e instruções (só a última responde)':{...f,avaliacao_evento:'ficticio',conversa:'Paciente: Quero cancelar.\nClara: '+last,pendente:patient},'Montar o pedido para a IA':{agenda_ok:true}};
 r.push({teste:'cancelamento sem aceite',last,patient,resultado:run('Decidir a ação',{acao:'cancelar',mensagem1:'Cancelada.'},refs)[0].json.rota});
}
for (const text of ["I'll forward your message to the doctor.",'Voy a pasar su mensaje a la doctora.','Vou passar sua mensagem para a doutora.'])
 r.push({teste:'promessa de encaminhamento',text,rota:run('Decidir a ação',{acao:'responder',mensagem1:text},{'Ler ficha e instruções (só a última responde)':f,'Montar o pedido para a IA':{agenda_ok:true}})[0].json.rota});
const err='Falha fictícia: body=Paciente Teste Codex; telefone=554199900951; queixa=sangramento';
const alert=nodes['Avisar a Keshion da falha'];
if(alert) r.push({teste:'erro livre no alerta',vazaDados:alert.parameters.jsonBody.includes('.slice(0, 120)'),exemploErro:err});
console.log(JSON.stringify(r,null,2));
