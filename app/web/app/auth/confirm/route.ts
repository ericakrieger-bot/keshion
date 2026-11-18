import type { EmailOtpType } from "@supabase/supabase-js";
import { redirect } from "next/navigation";
import type { NextRequest } from "next/server";
import { criarClienteServidor } from "@/lib/supabase/servidor";

// Destino do link que vai no e-mail (criar ou refazer a senha). Aceita os dois formatos do Supabase:
//  - ?code=...        (e-mail padrão do Supabase; precisa abrir no mesmo navegador que pediu o link)
//  - ?token_hash=...&type=...  (modelo próprio de e-mail, quando houver serviço de envio da Keshion; funciona em qualquer aparelho)
export async function GET(request: NextRequest) {
  const parametros = request.nextUrl.searchParams;
  const codigo = parametros.get("code");
  const tokenHash = parametros.get("token_hash");
  const tipo = parametros.get("type") as EmailOtpType | null;
  const proximo = parametros.get("next") ?? "/conversas";
  // só caminhos dentro do próprio app (evita mandar a pessoa para outro site)
  const destino = proximo.startsWith("/") && !proximo.startsWith("//") ? proximo : "/conversas";

  const supabase = await criarClienteServidor();
  if (codigo) {
    const { error } = await supabase.auth.exchangeCodeForSession(codigo);
    if (!error) redirect(destino);
  } else if (tokenHash && tipo) {
    const { error } = await supabase.auth.verifyOtp({ type: tipo, token_hash: tokenHash });
    if (!error) redirect(destino);
  }
  redirect("/login?erro=link");
}
