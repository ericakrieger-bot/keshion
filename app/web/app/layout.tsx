import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Keshion AI", template: "%s | Keshion AI" },
  description: "Conversas, agenda, pacientes e orçamentos da sua clínica, com a assistente Keshion AI.",
  applicationName: "Keshion AI",
  robots: { index: false, follow: false }, // app com login: fora dos buscadores
};

export const viewport: Viewport = {
  themeColor: "#0B1126",
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
