import { Logo, Simbolo } from "@/components/Marca";
import { Abas } from "@/components/Abas";
import { criarClienteServidor } from "@/lib/supabase/servidor";
import { saudacao } from "@/lib/formato";
import { sair } from "../login/acoes";

// Moldura do app: barra lateral (computador) ou abas embaixo (celular), nome da clínica e rodapé da Keshion.
export default async function LayoutApp({ children }: LayoutProps<"/">) {
  const supabase = await criarClienteServidor();
  const { data: { user } } = await supabase.auth.getUser();
  const { data: acessos } = await supabase.from("membros").select("papel, clinicas(id, nome)").limit(1);
  const clinicaBruta = acessos?.[0]?.clinicas;
  const clinica: { id: string; nome: string } | null = Array.isArray(clinicaBruta) ? clinicaBruta[0] ?? null : clinicaBruta ?? null;
  const nome = (user?.user_metadata?.nome as string | undefined) ?? "";

  if (!clinica) {
    return (
      <main className="login">
        <div className="box">
          <Logo />
          <div>
            <h1>Falta ligar o seu acesso</h1>
            <p className="sub">Você entrou, mas este e-mail ainda não está ligado a nenhuma clínica. Fale com a Keshion: contato@keshion.com.</p>
          </div>
          <form action={sair}><button className="btn soft" type="submit">Sair</button></form>
        </div>
      </main>
    );
  }

  const { count } = await supabase.from("encaminhamentos").select("id", { count: "exact", head: true }).is("resolvido", null);
  const pendentes = count ?? 0;

  return (
    <>
      <div className="shell">
        <aside className="side" aria-label="Navegação">
          <div className="brand"><Logo /></div>
          <Abas variante="lateral" pendentes={pendentes} />
        </aside>
        <main className="main">
          <div className="top">
            <Simbolo tamanho={32} />
            <div className="hello">
              <small>{saudacao()}{nome ? `, ${nome}` : ""}</small>
              <b>{clinica.nome}</b>
            </div>
            <form action={sair}><button className="sair" type="submit">Sair</button></form>
          </div>
          {children}
          <footer className="foot">
            <Logo />
            <span>App da {clinica.nome} · app.keshion.com</span>
          </footer>
        </main>
      </div>
      <Abas variante="barra" pendentes={pendentes} />
    </>
  );
}
