"use server";

import { criarClienteServidor } from "@/lib/supabase/servidor";

export type EstadoEsqueci = { erro?: string; enviado?: boolean } | undefined;

export async function pedirNovaSenha(_anterior: EstadoEsqueci, dados: FormData): Promise<EstadoEsqueci> {
  const email = String(dados.get("email") ?? "").trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) return { erro: "Confira o e-mail digitado." };

  const supabase = await criarClienteServidor();
  const { error } = await supabase.auth.resetPasswordForEmail(email);
  if (error?.status === 429) return { erro: "Muitos pedidos seguidos. Espere alguns minutos e tente de novo." };
  // A resposta é a mesma exista o e-mail ou não: assim ninguém descobre quem é cliente.
  return { enviado: true };
}
