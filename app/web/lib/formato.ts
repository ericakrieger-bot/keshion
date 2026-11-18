const FUSO = "America/Sao_Paulo";

export function iniciais(nome: string): string {
  return nome.split(" ").filter(Boolean).map((p) => p[0]).slice(0, 2).join("").toUpperCase();
}

export function primeiroNome(nome: string): string {
  return nome.split(" ")[0] ?? nome;
}

// "há 8 min", "há 3 h", "há 2 dias"
export function haQuanto(iso: string, agora = Date.now()): string {
  const min = Math.max(0, Math.round((agora - new Date(iso).getTime()) / 60000));
  if (min < 60) return `há ${min} min`;
  const h = Math.round(min / 60);
  if (h < 24) return `há ${h} h`;
  const d = Math.round(h / 24);
  return `há ${d} ${d === 1 ? "dia" : "dias"}`;
}

export function minutosDesde(iso: string, agora = Date.now()): number {
  return Math.max(0, Math.round((agora - new Date(iso).getTime()) / 60000));
}

// 14:05 no horário de Brasília; se não for de hoje, mostra a data (17/11).
export function horaOuData(iso: string, agora = new Date()): string {
  const d = new Date(iso);
  const dia = (x: Date) => new Intl.DateTimeFormat("pt-BR", { timeZone: FUSO }).format(x);
  if (dia(d) === dia(agora)) {
    return new Intl.DateTimeFormat("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: FUSO }).format(d);
  }
  return new Intl.DateTimeFormat("pt-BR", { day: "2-digit", month: "2-digit", timeZone: FUSO }).format(d);
}

export function saudacao(agora = new Date()): string {
  const hora = Number(new Intl.DateTimeFormat("pt-BR", { hour: "numeric", hour12: false, timeZone: FUSO }).format(agora));
  return hora < 12 ? "Bom dia" : hora < 18 ? "Boa tarde" : "Boa noite";
}
