"use server";

import { revalidatePath } from "next/cache";
import { criarClienteServidor } from "@/lib/supabase/servidor";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

// Marca um encaminhamento como resolvido. As regras do banco garantem que só vale para a clínica de quem está logado.
export async function resolverEncaminhamento(dados: FormData) {
  const id = String(dados.get("id") ?? "");
  if (!UUID.test(id)) return;
  const supabase = await criarClienteServidor();
  await supabase.from("encaminhamentos").update({ resolvido: new Date().toISOString() }).eq("id", id);
  revalidatePath("/conversas");
}
