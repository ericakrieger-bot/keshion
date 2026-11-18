"use client";

import { useActionState, useState } from "react";
import { salvarNovaSenha, type EstadoNovaSenha } from "./acoes";

export function FormularioNovaSenha() {
  const [estado, acao, pendente] = useActionState<EstadoNovaSenha, FormData>(salvarNovaSenha, undefined);
  const [mostrar, setMostrar] = useState(false);
  const tipo = mostrar ? "text" : "password";
  return (
    <form action={acao}>
      <div>
        <label className="lbl" htmlFor="senha">Nova senha</label>
        <input className="inp" id="senha" name="senha" type={tipo} autoComplete="new-password" minLength={10} required />
      </div>
      <div>
        <label className="lbl" htmlFor="repetida">Repita a nova senha</label>
        <input className="inp" id="repetida" name="repetida" type={tipo} autoComplete="new-password" minLength={10} required />
        <label className="check" style={{ marginTop: 8, fontSize: 14 }}>
          <input type="checkbox" checked={mostrar} onChange={(e) => setMostrar(e.target.checked)} />
          Mostrar as senhas
        </label>
      </div>
      <span className="err" aria-live="polite">{estado?.erro}</span>
      <button className="btn dark" type="submit" disabled={pendente}>
        {pendente ? "Salvando..." : "Salvar e entrar"}
      </button>
    </form>
  );
}
