"use server";

import { redirect } from "next/navigation";
import { criarClienteServidor } from "@/lib/supabase/servidor";

export type EstadoNovaSenha = { erro?: string } | undefined;

const MINIMO = 10;

export async function salvarNovaSenha(_anterior: EstadoNovaSenha, dados: FormData): Promise<EstadoNovaSenha> {
  const senha = String(dados.get("senha") ?? "");
  const repetida = String(dados.get("repetida") ?? "");
  if (senha.length < MINIMO) return { erro: `Use pelo menos ${MINIMO} caracteres.` };
  if (senha !== repetida) return { erro: "As duas senhas não são iguais." };

  const supabase = await criarClienteServidor();
  const { error } = await supabase.auth.updateUser({ password: senha });
  if (error) {
    if (error.code === "same_password") return { erro: "Escolha uma senha diferente da anterior." };
    if (error.code === "weak_password") return { erro: "Essa senha é fraca. Misture letras, números e símbolos." };
    return { erro: "Não foi possível salvar agora. Peça um novo link em \"Esqueci a senha\"." };
  }
  redirect("/conversas");
}
