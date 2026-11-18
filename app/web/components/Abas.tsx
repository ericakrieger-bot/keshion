"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconeAgenda, IconeConversas, IconeOrcamentos, IconePacientes, IconePainel, IconeReativar,
} from "./Icones";

const ABAS = [
  { href: "/conversas", nome: "Conversas", icone: <IconeConversas /> },
  { href: "/agenda", nome: "Agenda", icone: <IconeAgenda /> },
  { href: "/pacientes", nome: "Pacientes", icone: <IconePacientes /> },
  { href: "/orcamentos", nome: "Orçamentos", icone: <IconeOrcamentos /> },
  { href: "/reativar", nome: "Reativar", icone: <IconeReativar /> },
  { href: "/painel", nome: "Painel", icone: <IconePainel /> },
];

// variante "lateral": barra do computador. variante "barra": abas fixas embaixo, no celular.
export function Abas({ variante, pendentes }: { variante: "lateral" | "barra"; pendentes: number }) {
  const caminho = usePathname();
  const lateral = variante === "lateral";
  const itens = ABAS.map((aba) => {
    const ativa = caminho === aba.href || caminho.startsWith(aba.href + "/");
    const contador = aba.href === "/conversas" && pendentes > 0 ? (
      <b className="cnt" aria-label={`${pendentes} precisam de você`}>{pendentes}</b>
    ) : null;
    return (
      <Link key={aba.href} href={aba.href} className={lateral ? "sd" : "dk"} aria-current={ativa ? "page" : undefined}>
        {aba.icone}
        {lateral ? aba.nome : <span>{aba.nome}</span>}
        {contador}
      </Link>
    );
  });
  return lateral ? <div>{itens}</div> : <nav className="dock" aria-label="Seções">{itens}</nav>;
}
