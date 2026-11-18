import type { NextConfig } from "next";
import path from "node:path";

// O app inteiro fica atrás de login e mostra dados de cada clínica: nada dele pode ser guardado em cache
// compartilhado. Por isso o modo "Cache Components" (que o modelo do Next traz ligado) fica desligado:
// cada tela é montada na hora, com os dados de quem está logado.
const nextConfig: NextConfig = {
  turbopack: { root: path.join(__dirname) },
};

export default nextConfig;
