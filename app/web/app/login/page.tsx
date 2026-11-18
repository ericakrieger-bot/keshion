import type { Metadata } from "next";
import { Logo } from "@/components/Marca";
import { FormularioLogin } from "./formulario";

export const metadata: Metadata = { title: "Entrar" };

export default function PaginaLogin() {
  return (
    <main className="login">
      <div className="box">
        <Logo />
        <div>
          <h1>Entrar</h1>
          <p className="sub">Use o e-mail e a senha que a Keshion enviou para a sua clínica.</p>
        </div>
        <FormularioLogin />
        <p className="note">Esqueceu a senha? Fale com a Keshion: contato@keshion.com.</p>
      </div>
    </main>
  );
}
