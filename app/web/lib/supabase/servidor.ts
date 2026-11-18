import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

// Cliente do Supabase para telas e ações do servidor. Usa só a chave pública: quem protege os dados
// são as regras por clínica no banco (RLS), que enxergam o usuário logado.
export async function criarClienteServidor() {
  const jar = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
    {
      cookies: {
        getAll: () => jar.getAll(),
        setAll(lista) {
          try {
            lista.forEach(({ name, value, options }) => jar.set(name, value, options));
          } catch {
            // Chamado de uma tela (só leitura): quem renova a sessão é o proxy.ts.
          }
        },
      },
    },
  );
}
