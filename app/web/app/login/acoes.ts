"use server";

import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/servidor";

export type EstadoLogin = { erro?: string } | undefined;

export async function entrar(_anterior: EstadoLogin, dados: FormData): Promise<EstadoLogin> {
  const email = String(dados.get("email") ?? "").trim();
  const senha = String(dados.get("senha") ?? "");
  if (!email || !senha) return { erro: "Digite o e-mail e a senha." };

  const supabase = await criarClienteServidor();
  const { error } = await supabase.auth.signInWithPassword({ email, password: senha });
  if (error) return { erro: "E-mail ou senha incorretos." };

  redirect("/conversas");
}

export async function sair() {
  const supabase = await criarClienteServidor();
  await supabase.auth.signOut();
  redirect("/login");
}
