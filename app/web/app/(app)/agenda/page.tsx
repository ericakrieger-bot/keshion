import type { Metadata } from "next";
import { EmConstrucao } from "@/components/EmConstrucao";

export const metadata: Metadata = { title: "Agenda" };

export default function PaginaAgenda() {
  return <EmConstrucao titulo="Agenda do dia" descricao="Consultas de hoje e amanhã, confirmações, compareceu e faltou." quando="dezembro" />;
}
