import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

// Roda antes de cada tela: renova a sessão e manda para o login quem não entrou.
// (No Next 16 o arquivo se chama proxy.ts; antes era middleware.ts.)
export async function proxy(request: NextRequest) {
  let resposta = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll(lista) {
          lista.forEach(({ name, value }) => request.cookies.set(name, value));
          resposta = NextResponse.next({ request });
          lista.forEach(({ name, value, options }) => resposta.cookies.set(name, value, options));
        },
      },
    },
  );

  const { data } = await supabase.auth.getClaims();
  const logado = Boolean(data?.claims);
  const noLogin = request.nextUrl.pathname === "/login";

  // Deslogado fora do login vai para o login; logado no login vai para as conversas.
  if (logado === noLogin) {
    const destino = request.nextUrl.clone();
    destino.pathname = logado ? "/conversas" : "/login";
    destino.search = "";
    const redirecionar = NextResponse.redirect(destino);
    resposta.cookies.getAll().forEach((cookie) => redirecionar.cookies.set(cookie));
    return redirecionar;
  }
  return resposta;
}

export const config = {
  matcher: [
    // tudo, menos arquivos estáticos, ícones, fontes e o manifesto do PWA
    "/((?!_next/static|_next/image|favicon.ico|icon.svg|apple-icon.png|manifest.webmanifest|fonts/|icons/).*)",
  ],
};
