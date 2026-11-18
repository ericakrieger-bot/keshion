"use client";

import { useActionState } from "react";
import { pedirNovaSenha, type EstadoEsqueci } from "./acoes";

export function FormularioEsqueci() {
  const [estado, acao, pendente] = useActionState<EstadoEsqueci, FormData>(pedirNovaSenha, undefined);
  if (estado?.enviado) {
    return (
      <div className="card">
        <b>Pedido enviado</b>
        <p className="note">Se esse e-mail estiver cadastrado, enviamos agora um link para criar uma nova senha. Confira a caixa de entrada e o spam. O link vale por pouco tempo e só funciona uma vez.</p>
      </div>
    );
  }
  return (
    <form action={acao}>
      <div>
        <label className="lbl" htmlFor="email">E-mail</label>
        <input className="inp" id="email" name="email" type="email" autoComplete="username" required />
      </div>
      <span className="err" aria-live="polite">{estado?.erro}</span>
      <button className="btn dark" type="submit" disabled={pendente}>
        {pendente ? "Enviando..." : "Enviar o link"}
      </button>
    </form>
  );
}
