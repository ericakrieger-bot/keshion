import type { Metadata } from "next";
import { Logo } from "@/components/Marca";
import { FormularioNovaSenha } from "./formulario";

export const metadata: Metadata = { title: "Nova senha" };

// Só chega aqui quem abriu o link do e-mail (o proxy manda para o login quem não tem sessão).
export default function PaginaNovaSenha() {
  return (
    <main className="login">
      <div className="box">
        <Logo />
        <div>
          <h1>Crie a sua senha</h1>
          <p className="sub">Use pelo menos 10 caracteres. Um cofre de senhas ajuda a não esquecer.</p>
        </div>
        <FormularioNovaSenha />
      </div>
    </main>
  );
}
