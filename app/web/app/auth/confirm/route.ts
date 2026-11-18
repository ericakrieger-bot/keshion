import type { EmailOtpType } from "@supabase/supabase-js";
import { redirect } from "next/navigation";
import type { NextRequest } from "next/server";
import { criarClienteServidor } from "@/lib/supabase/servidor";

// Destino do link que vai no e-mail (criar ou refazer a senha). O link traz um código de uso único (token_hash);
// aqui ele é trocado por uma sessão e a pessoa segue para a tela de nova senha.
export async function GET(request: NextRequest) {
  const parametros = request.nextUrl.searchParams;
  const tokenHash = parametros.get("token_hash");
  const tipo = parametros.get("type") as EmailOtpType | null;
  const proximo = parametros.get("next") ?? "/conversas";
  // só caminhos dentro do próprio app (evita mandar a pessoa para outro site)
  const destino = proximo.startsWith("/") && !proximo.startsWith("//") ? proximo : "/conversas";

  if (tokenHash && tipo) {
    const supabase = await criarClienteServidor();
    const { error } = await supabase.auth.verifyOtp({ type: tipo, token_hash: tokenHash });
    if (!error) redirect(destino);
  }
  redirect("/login?erro=link");
}
