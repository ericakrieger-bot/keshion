import type { MetadataRoute } from "next";

// Faz o app poder ser instalado no celular (PWA). Valores do kit de marca (branding/kit/digital/site.webmanifest).
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Keshion AI",
    short_name: "Keshion",
    description: "Conversas, agenda, pacientes e orçamentos da sua clínica.",
    start_url: "/",
    scope: "/",
    display: "standalone",
    background_color: "#0B1126",
    theme_color: "#0B1126",
    lang: "pt-BR",
    icons: [
      { src: "/icons/app-icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icons/app-icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icons/app-icon-maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
  };
}
