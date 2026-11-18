import type { Metadata } from "next";
import Link from "next/link";
import { criarClienteServidor } from "@/lib/supabase/servidor";
import { haQuanto, horaOuData, iniciais, minutosDesde, primeiroNome } from "@/lib/formato";
import { IconeOk, IconeRelogio, IconeTelefone, IconeConversas } from "@/components/Icones";
import { resolverEncaminhamento } from "./acoes";

export const metadata: Metadata = { title: "Conversas" };

type Paciente = { id: string; nome: string | null; nome_completo: string | null; telefone?: string; ja_paciente?: boolean; situacao?: string };
const umPaciente = (x: unknown): Paciente | null => (Array.isArray(x) ? (x[0] ?? null) : ((x as Paciente) ?? null));
const nomeDe = (p: Paciente | null) => p?.nome_completo || p?.nome || "Paciente sem nome";

const TIPOS: Record<string, { rotulo: string; tag: string; urgente: boolean }> = {
  urgencia: { rotulo: "Urgência", tag: "t-late", urgente: true },
  pediu_doutora: { rotulo: "Pediu a doutora", tag: "t-late", urgente: true },
  ia_nao_sabe: { rotulo: "A IA não sabe", tag: "t-warn", urgente: false },
  desconto: { rotulo: "Pedido de desconto", tag: "t-info", urgente: false },
  reclamacao: { rotulo: "Reclamação", tag: "t-warn", urgente: false },
  outro: { rotulo: "Outro assunto", tag: "t-neutral", urgente: false },
};
const ESTADOS: Record<string, { rotulo: string; tag: string }> = {
  ia_respondeu: { rotulo: "IA respondeu", tag: "t-acc" },
  agendou: { rotulo: "Agendou", tag: "t-good" },
  aguardando_equipe: { rotulo: "Aguardando a equipe", tag: "t-warn" },
  equipe_assumiu: { rotulo: "A equipe assumiu", tag: "t-neutral" },
};

export default async function Conversas({ searchParams }: PageProps<"/conversas">) {
  const { f } = await searchParams;
  const filtro = f === "fora" || f === "assumidas" ? f : "todas";
  const supabase = await criarClienteServidor();

  const [{ data: encaminhamentos }, { data: conversas }] = await Promise.all([
    supabase
      .from("encaminhamentos")
      .select("id, tipo, mensagem, criado, pacientes(id, nome, nome_completo, telefone, ja_paciente, situacao)")
      .is("resolvido", null)
      .order("criado", { ascending: true }),
    supabase
      .from("conversas")
      .select("estado, ultima_mensagem, ultimo_horario, fora_do_horario, pacientes(id, nome, nome_completo)")
      .order("ultimo_horario", { ascending: false })
      .limit(100),
  ]);

  const agora = Date.now();
  const abertos = [...(encaminhamentos ?? [])].sort((a, b) => {
    const ua = TIPOS[a.tipo]?.urgente ? 0 : 1;
    const ub = TIPOS[b.tipo]?.urgente ? 0 : 1;
    return ua - ub || new Date(a.criado).getTime() - new Date(b.criado).getTime();
  });
  const maisAntiga = abertos.reduce((m, x) => Math.max(m, minutosDesde(x.criado, agora)), 0);

  const todas = conversas ?? [];
  const contagens = {
    todas: todas.length,
    fora: todas.filter((c) => c.fora_do_horario).length,
    assumidas: todas.filter((c) => c.estado === "equipe_assumiu").length,
  };
  const lista = todas.filter((c) => (filtro === "fora" ? c.fora_do_horario : filtro === "assumidas" ? c.estado === "equipe_assumiu" : true));

  return (
    <>
      <div>
        <h1>Conversas</h1>
        <p className="sub">A IA responde sozinha. Em cima fica só o que foi encaminhado para a equipe.</p>
      </div>

      <div className="grid2">
        <div className="stack">
          <section className="hero" aria-label="Encaminhadas para a equipe">
            <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "space-between", gap: 10, flexWrap: "wrap" }}>
              <div><p>Precisa de você</p><div className="big">{abertos.length}</div></div>
              {abertos.length > 0 && <span className="chipline"><IconeRelogio /> a mais antiga {haQuanto(new Date(agora - maisAntiga * 60000).toISOString(), agora)}</span>}
            </div>
          </section>

          <div className="stack">
            {abertos.length === 0 && (
              <div className="card empty"><b>Tudo em dia</b><p>Quando algo for encaminhado para a equipe, aparece aqui.</p></div>
            )}
            {abertos.map((x) => {
              const p = umPaciente(x.pacientes);
              const tipo = TIPOS[x.tipo] ?? TIPOS.outro;
              const espera = minutosDesde(x.criado, agora);
              const fone = p?.telefone?.replace(/\D/g, "");
              return (
                <article className="card" key={x.id}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
                    <span className={`tag ${tipo.tag}`}>{tipo.rotulo}</span>
                    <span className={`tag ${espera > 15 ? "t-late" : "t-neutral"}`}><IconeRelogio /> {espera} min</span>
                  </div>
                  <div className="person">
                    <span className="avatar sm" aria-hidden="true">{iniciais(nomeDe(p))}</span>
                    <span className="nm">
                      <b>{nomeDe(p)}</b>
                      <small>{p?.ja_paciente ? "Já é paciente" : "Novo contato"}{p?.situacao ? ` · ${p.situacao}` : ""}</small>
                    </span>
                  </div>
                  {x.mensagem && <p className="quote"><em>Mensagem do paciente</em>{x.mensagem}</p>}
                  <div className="acts">
                    {fone && <a className="btn acc" href={`https://wa.me/${fone}`} target="_blank" rel="noopener noreferrer"><IconeConversas />Abrir no WhatsApp</a>}
                    {fone && <a className="btn round" href={`tel:+${fone}`} aria-label={`Ligar para ${primeiroNome(nomeDe(p))}`}><IconeTelefone /></a>}
                    <form action={resolverEncaminhamento}>
                      <input type="hidden" name="id" value={x.id} />
                      <button className="btn round" type="submit" aria-label="Marcar como resolvido"><IconeOk /></button>
                    </form>
                  </div>
                </article>
              );
            })}
          </div>
        </div>

        <div className="stack">
          <div className="sec"><h2>Todas as conversas</h2><span>recentes</span></div>
          <div className="pills" role="group" aria-label="Filtrar conversas">
            {([["todas", "Todas"], ["fora", "Fora do horário"], ["assumidas", "A equipe assumiu"]] as const).map(([chave, rotulo]) => (
              <Link key={chave} href={chave === "todas" ? "/conversas" : `/conversas?f=${chave}`} className="pill" aria-pressed={filtro === chave}>
                {rotulo} <i>{contagens[chave]}</i>
              </Link>
            ))}
          </div>
          <div className="card list">
            {lista.length === 0 && <div className="empty"><b>Nenhuma conversa aqui</b><p>Troque o filtro para ver as outras.</p></div>}
            {lista.map((c, i) => {
              const p = umPaciente(c.pacientes);
              const estado = ESTADOS[c.estado] ?? ESTADOS.ia_respondeu;
              return (
                <div className="conv" key={`${p?.id ?? i}`}>
                  <span className="avatar sm" aria-hidden="true">{iniciais(nomeDe(p))}</span>
                  <span className="nm">
                    <span style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                      <b>{nomeDe(p)}</b><time dateTime={c.ultimo_horario}>{horaOuData(c.ultimo_horario)}</time>
                    </span>
                    <p>{c.ultima_mensagem}</p>
                    <span className={`tag ${estado.tag}`} style={{ marginTop: 6 }}>{estado.rotulo}</span>
                    {c.fora_do_horario && <> <span className="tag t-neutral" style={{ marginTop: 6 }}>Fora do horário</span></>}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </>
  );
}
