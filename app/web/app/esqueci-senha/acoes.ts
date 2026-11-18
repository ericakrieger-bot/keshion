"use server";

import { headers } from "next/headers";
import { criarClienteServidor } from "@/lib/supabase/servidor";

export type EstadoEsqueci = { erro?: string; enviado?: boolean } | undefined;

export async function pedirNovaSenha(_anterior: EstadoEsqueci, dados: FormData): Promise<EstadoEsqueci> {
  const email = String(dados.get("email") ?? "").trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) return { erro: "Confira o e-mail digitado." };

  // O link do e-mail volta para o mesmo endereço de onde o pedido saiu e abre direto a tela de nova senha.
  // O endereço precisa estar na lista de redirecionamentos permitidos do Supabase.
  const h = await headers();
  const host = h.get("x-forwarded-host") ?? h.get("host");
  const protocolo = h.get("x-forwarded-proto") ?? (host?.startsWith("localhost") ? "http" : "https");
  const redirectTo = host ? `${protocolo}://${host}/auth/confirm?next=/nova-senha` : undefined;

  const supabase = await criarClienteServidor();
  const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo });
  if (error) {
    // O motivo real fica só no registro do servidor (nunca na tela), para a Keshion investigar e-mail que não chega.
    console.error("[esqueci-senha] o Supabase recusou o pedido:", error.status, error.code, error.message);
    if (error.status === 429) return { erro: "Muitos pedidos seguidos. Espere alguns minutos e tente de novo." };
    // Falha do sistema (sem conexão ou erro do servidor): avisa, porque o e-mail não saiu. Não revela se o e-mail existe.
    if (!error.status || error.status >= 500) return { erro: "Não conseguimos enviar agora. Tente de novo em alguns minutos." };
  }
  // A resposta é a mesma exista o e-mail ou não: assim ninguém descobre quem é cliente.
  return { enviado: true };
}
