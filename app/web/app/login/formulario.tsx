"use client";

import { useActionState, useState } from "react";
import { entrar, type EstadoLogin } from "./acoes";

export function FormularioLogin() {
  const [estado, acao, pendente] = useActionState<EstadoLogin, FormData>(entrar, undefined);
  const [mostrar, setMostrar] = useState(false);
  return (
    <form action={acao}>
      <div>
        <label className="lbl" htmlFor="email">E-mail</label>
        <input className="inp" id="email" name="email" type="email" autoComplete="username" required />
      </div>
      <div>
        <label className="lbl" htmlFor="senha">Senha</label>
        <input className="inp" id="senha" name="senha" type={mostrar ? "text" : "password"} autoComplete="current-password" required />
        <label className="check" style={{ marginTop: 8, fontSize: 14 }}>
          <input type="checkbox" checked={mostrar} onChange={(e) => setMostrar(e.target.checked)} />
          Mostrar a senha
        </label>
      </div>
      <span className="err" aria-live="polite">{estado?.erro}</span>
      <button className="btn dark" type="submit" disabled={pendente}>
        {pendente ? "Entrando..." : "Entrar"}
      </button>
    </form>
  );
}
