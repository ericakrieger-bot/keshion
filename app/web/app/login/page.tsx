import type { Metadata } from "next";
import Link from "next/link";
import { Logo } from "@/components/Marca";
import { FormularioLogin } from "./formulario";

export const metadata: Metadata = { title: "Entrar" };

export default async function PaginaLogin({ searchParams }: PageProps<"/login">) {
  const { erro } = await searchParams;
  return (
    <main className="login">
      <div className="box">
        <Logo />
        <div>
          <h1>Entrar</h1>
          <p className="sub">Use o e-mail e a senha que a Keshion enviou para a sua clínica.</p>
        </div>
        {erro === "link" && <p className="err">Esse link expirou ou já foi usado. Peça um novo em "Esqueci a senha".</p>}
        <FormularioLogin />
        <p className="note"><Link href="/esqueci-senha" className="how">Esqueci a senha</Link></p>
      </div>
    </main>
  );
}
