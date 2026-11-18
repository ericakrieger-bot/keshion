# App da Keshion (app.keshion.com)

Começado em 18/11/2026. Protótipo de referência: `../app-crm-painel/prototipo-crm-mobile.html` (desenho e textos das telas). Decisões: `../app-crm-painel/RESUMO-HOSPEDAGEM-E-DECISOES-APP.md`.

## Pastas

| Onde | O quê |
|---|---|
| `web/` | O app (Next.js 16, TypeScript). Telas em `web/app/(app)/`, login em `web/app/login/`, proxy de sessão em `web/proxy.ts` |
| `supabase/schema.sql` | Banco do app (tabelas, regras por clínica, função da Clara). Já aplicado no projeto `keshion-app` |
| `supabase/teste-isolamento.sql` | Teste do banco: desfaz tudo no final. Rodar depois de mudar o schema |
| `supabase/dados-demo.sql` | Clínica de demonstração fictícia (Dra. Suzana Vidal) |

## Rodar no computador

```bash
cd app/web
npm install
npm run dev -- -p 3100
```

Precisa do arquivo `app/web/.env.local` (fora do Git) com `NEXT_PUBLIC_SUPABASE_URL` e `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`. Os valores estão no `.env` da raiz do projeto. Só a chave pública entra no app; a chave secreta nunca.

## Estado (18/11/2026)

- Pronto: login por e-mail e senha, proteção de todas as telas, moldura com as 6 abas (barra lateral no computador, abas embaixo no celular), logo e fontes da marca, instalação como app (PWA), tela de Conversas lendo do banco.
- Em construção: Agenda, Pacientes (dezembro); Orçamentos, Reativar, Painel (janeiro).
- Pendente: ligar a Clara ao app (avisos nos dois sentidos), publicar na Netlify, desligar o cadastro público no Supabase.

## Cuidados

- O Next 16 mudou: o arquivo antigo `middleware.ts` agora é `proxy.ts`, e `cookies()` é assíncrono. Antes de escrever código novo, consultar `web/node_modules/next/dist/docs/`.
- O modo "Cache Components" fica desligado de propósito (`web/next.config.ts`): tudo aqui depende de quem está logado.
