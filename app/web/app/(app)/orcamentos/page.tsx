import type { Metadata } from "next";
import { EmConstrucao } from "@/components/EmConstrucao";

export const metadata: Metadata = { title: "Orçamentos" };

export default function PaginaOrcamentos() {
  return <EmConstrucao titulo="Orçamentos" descricao="Orçamentos em PDF, lembretes da IA e o que foi aceito ou recusado." quando="janeiro" />;
}
