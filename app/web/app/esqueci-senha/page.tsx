import type { Metadata } from "next";
import Link from "next/link";
import { Logo } from "@/components/Marca";
import { FormularioEsqueci } from "./formulario";

export const metadata: Metadata = { title: "Esqueci a senha" };

export default function PaginaEsqueci() {
  return (
    <main className="login">
      <div className="box">
        <Logo />
        <div>
          <h1>Esqueci a senha</h1>
          <p className="sub">Digite o e-mail do seu acesso. Você recebe um link para criar uma nova senha, é só clicar.</p>
        </div>
        <FormularioEsqueci />
        <p className="note"><Link href="/login" className="how">Voltar para o login</Link></p>
      </div>
    </main>
  );
}
