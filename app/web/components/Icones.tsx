// Ícones de traço simples (mesmos do protótipo). Herdam a cor do texto.
const base = { viewBox: "0 0 24 24", "aria-hidden": true } as const;

export const IconeConversas = () => (
  <svg {...base}><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z" /></svg>
);
export const IconeAgenda = () => (
  <svg {...base}><rect x="3.5" y="5" width="17" height="15.5" rx="3" /><path d="M3.5 10h17M8 3v4M16 3v4" /></svg>
);
export const IconePacientes = () => (
  <svg {...base}><circle cx="9" cy="8" r="3.5" /><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5M16 4.5a3.5 3.5 0 0 1 0 7M18.5 14.8c1.6.8 2.6 2.5 3 5.2" /></svg>
);
export const IconeOrcamentos = () => (
  <svg {...base}><path d="M6 3h8l4 4v14H6z" /><path d="M14 3v4h4M9 12h6M9 16h6" /></svg>
);
export const IconeReativar = () => (
  <svg {...base}><path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" /></svg>
);
export const IconePainel = () => (
  <svg {...base}><path d="M4 20V10M10 20V4M16 20v-7M22 20H2" /></svg>
);
export const IconeTelefone = () => (
  <svg {...base}><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" /></svg>
);
export const IconeOk = () => (
  <svg {...base}><path d="M5 12l5 5 9-10" /></svg>
);
export const IconeRelogio = () => (
  <svg {...base} style={{ width: 14, height: 14 }}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></svg>
);
