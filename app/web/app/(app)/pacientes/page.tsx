import type { Metadata } from "next";
import { EmConstrucao } from "@/components/EmConstrucao";

export const metadata: Metadata = { title: "Pacientes" };

export default function PaginaPacientes() {
  return <EmConstrucao titulo="Pacientes" descricao="Cadastro, situação, tratamento, orçamento e histórico de cada paciente." quando="dezembro" />;
}
