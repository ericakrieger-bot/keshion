import type { Metadata } from "next";
import { EmConstrucao } from "@/components/EmConstrucao";

export const metadata: Metadata = { title: "Painel" };

export default function PaginaPainel() {
  return <EmConstrucao titulo="Painel" descricao="Os números da clínica e onde a assistente ajudou." quando="janeiro" />;
}
