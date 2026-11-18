import type { Metadata } from "next";
import { EmConstrucao } from "@/components/EmConstrucao";

export const metadata: Metadata = { title: "Reativar" };

export default function PaginaReativar() {
  return <EmConstrucao titulo="Reativar pacientes" descricao="Pacientes antigos com limpeza, manutenção ou consulta vencida." quando="janeiro" />;
}
