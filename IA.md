# IA.md - Contexto Operacional

## Estado atual (resumo vivo)

<!--
  EXCECAO a regra append-only desta secao: ela e um RESUMO reescrevivel.
  Responde "onde o projeto esta AGORA" em poucas linhas, para retomar contexto
  sem reler toda a linha do tempo abaixo. Reescreva-a a cada mudanca de estado.
-->

[2026-07-28] Landing page do Prisma concluida em `frontend/` (React 19 + TypeScript + Vite 8 + Tailwind 4 + Motion 12), com identidade visual do documento UX/UI aplicada, secoes de tela cheia e tela de escolha de perfil. Backend nao existe: e escopo do Felipe. Proximo passo do frontend: publicar os mockups do `Estudo-com-IA` e preencher `BASE_DESTINOS`.

## Objetivo do projeto

[2026-07-28] Implementacao web do produto concebido em `Estudo-com-IA`: plataforma SaaS de estudos para instituicoes de ensino usando **OpenRouter como motor de IA**. A instituicao assina, recebe creditos de IA, e o diretor distribui para professores (gerar/corrigir provas e material) e alunos (tutor com memoria persistente). Tres perfis de login: aluno, professor, diretor.

O repositorio `Estudo-com-IA` mantem a documentacao de concepcao (visao, arquitetura, perfis, creditos, memoria, roadmap) e um mockup HTML estatico. Este repositorio contem o codigo real.

## Estado atual

- **Implementado**: landing page publica em `frontend/`, `start_app.py` na raiz.
- **Em progresso**: Fase 0 - falta o backend.
- **Pendente**: backend Django, autenticacao dos 3 perfis, gateway de IA.

## Stack e dependencias

- Frontend: React 19 + TypeScript + Vite 8 + Tailwind 4 (instalado, em `frontend/`)
- Backend: Django + Django REST Framework (monolito modular) - ainda nao iniciado
- Banco: PostgreSQL
- IA: OpenRouter (API unificada multi-modelo)
- Deploy: Railway
- Testes: a definir junto com o backend

## Decisoes de arquitetura

Herdadas da concepcao em `Estudo-com-IA/IA.md` e ainda validas:

- [2026-07-16] **OpenRouter como provedor unico de IA** - API unificada multi-modelo permite roteamento por classe de tarefa (tutoria, geracao, correcao, resumo) otimizando custo dos creditos. Mapeamento classe-modelo em configuracao, nao em codigo.
- [2026-07-16] **Credito como unidade interna** - conversao custo-do-modelo para creditos por tabela configuravel com margem; saldo derivado do ledger (fonte unica), debito so apos resposta bem-sucedida.
- [2026-07-16] **Memoria por resumos consolidados, nao conversa crua** - sessoes sao resumidas por modelo barato em registros imutaveis datados; recuperacao simples (materia/topico/recencia) antes de considerar embeddings.
- [2026-07-16] **Monolito modular primeiro** - sem microservicos/fila/cache ate gargalo real (principio "simplicidade verificavel" do `GUIA_MINIMO_QUALIDADE.md`).
- [2026-07-16] **Conteudo de IA nasce rascunho** - prova/nota so vale apos revisao explicita do professor (decisao pedagogica e de responsabilidade).
- [2026-07-16] **Gateway de IA no backend** - toda chamada de IA passa pelo backend; o frontend nunca fala com o OpenRouter diretamente.

Apps Django planejados: `contas`, `academico`, `conteudo`, `creditos`, `ia`, `memoria`.

## Decisoes de design e convencoes

- [2026-07-28] Padroes de qualidade sincronizados em `doktor SystemDesign/` via comando global `doktor`. A pasta e uma copia sincronizada, nao editavel neste projeto: mudancas de padrao vao no repositorio Doktor System-Design.
- [2026-07-28] Commits seguem Conventional Commits: `tipo(escopo): descricao no imperativo`.
- [2026-07-28] **Marca do produto: "Prisma"**. A metafora e a refracao - um tema entra, materiais de estudo saem em tres direcoes (aluno, professor, diretor). O logo e um prisma com feixe de entrada e espectro de saida nas tres cores de perfil.
- [2026-07-28] **Tailwind 4 com plugin `@tailwindcss/vite`**, nao PostCSS. A v4 dispensa `tailwind.config.js`: tokens ficam em `@theme` dentro de `frontend/src/index.css`. Versao confirmada na instalacao (4.3.3), nao presumida - v3 e v4 configuram de formas incompativeis.
- [2026-07-28] **Copy separada do JSX** em `frontend/src/content/landing.ts`. Editar texto da landing nao exige mexer em componente.
- [2026-07-28] **Um tom por perfil** (`--color-aluno`, `--color-professor`, `--color-diretor`) em vez de uma unica familia de cor, conforme `DESIGN_SYSTEM_FRONTEND.md` secao 4.
- [2026-07-28] **Depoimentos ficam como placeholder** ate a instituicao coletar relatos reais. Publicar depoimento ficticio como se fosse real e falso testemunho de cliente; os cards usam borda tracejada para deixar o estado pendente visivel.

- [2026-07-28] **Divisao de trabalho por camada**: Andre no frontend, Felipe no backend. Ao propor trabalho de backend (models, autenticacao, gateway de IA), declarar o contrato e o ponto de integracao em vez de implementar direto.
- [2026-07-28] **Paleta e tipografia passam a ser normativas**, conforme o documento de identidade UX/UI recebido: `#F7F5EE`, `#1A1A1A`, `#C85A3C`, `#6A8550`, `#7B78C8`; Josefin Sans em caixa alta com tracking `0.08em` nos titulos, Inter no corpo. Substitui os tons dessaturados que eu havia proposto antes - agora ha fonte de verdade escrita.
- [2026-07-28] **Contorno em grafite suavizado, nao `#1A1A1A` puro.** Desvio consciente do documento: preto solido em tela cheia pesa demais. A borda continua nitida e sem sombra difusa, que e o que define o estilo. Tokens `--color-contorno` e `--color-contorno-forte`.
- [2026-07-28] **Secoes em `min-h-svh`.** Secoes curtas deixavam a cor da secao seguinte vazar para o campo de visao. `svh` e nao `vh` porque a barra do navegador em celular provoca salto com `vh` fixo.
- [2026-07-28] **Motion (ex-Framer Motion) como biblioteca de animacao.** Custo real: bundle de 214 kB para ~354 kB (66 -> 112 kB comprimido). Aceito para landing; se performance virar prioridade, `motion/react-m` com carregamento sob demanda reduz.
- [2026-07-28] **Sem Lottie e sem three.js.** Ambos foram avaliados: sem alguem produzindo arquivos no After Effects, seriam dependencia morta no bundle. O prisma refratando e as letras 3D sao SVG e CSS. Se surgir producao de `.lottie`, `@lottiefiles/dotlottie-react` e o caminho.

### [2026-07-28] ACESSIBILIDADE: acento colorido nao serve para texto pequeno

CONTEXTO: o documento de identidade alerta para lavanda em texto pequeno. Medi o contraste dos tres acentos contra os fundos reais da pagina.
MEDICAO: terracota 3.21-4.15:1 | oliva 3.15-4.06:1 | lavanda 2.98-3.85:1. **Nenhum** atinge os 4.5:1 que a WCAG AA exige para texto pequeno - o problema e mais amplo do que o documento sugere. Lavanda sobre tint terracota (2.98) reprova ate para texto grande.
DECISAO: acento vive em marcador, faixa, filete, icone decorativo e borda. Texto legivel usa grafite ou `texto-secundario` (5.48-6.78:1). Registrado como regra 5 no topo de `index.css`, com a tabela.
VALIDACAO: script de contraste executado sobre os pares reais de cor; rotulos de perfil no demo migrados de acento para `texto-secundario`.

### [2026-07-28] Desempenho: a primeira versao das animacoes travava

CONTEXTO: com titulo letra a letra, atmosfera de quatro camadas e cards 3D, a pagina engasgava ao rolar.
CAUSAS: (a) cada letra desenhada 4x com `mix-blend-screen` - 160 nos de composicao num titulo de 40 letras; (b) `radial-gradient` remontado a cada quadro via `useMotionTemplate`, forcando repintura; (c) `mask-image` e `filter: blur` animados por scroll, das operacoes mais caras do CSS.
DECISAO: refracao por `text-shadow` (um no por letra); brilho especular por `transform` sobre gradiente fixo; portal so com `opacity` e `scale`; atmosfera de quatro camadas para duas, sem o grao em `mix-blend-overlay`.
VALIDACAO: build e lint limpos. **Pendente**: medicao real de FPS em navegador - nao foi possivel nesta sessao.

### [2026-07-28] Landing page: React desde o inicio, sem etapa em HTML puro

CONTEXTO: pedido de clonar uma landing page de referencia (Prism Labs, produto de terceiro). O repositorio ainda nao tinha frontend.
ALTERNATIVAS: (a) HTML unico com Tailwind por CDN, migrando para React depois; (b) ja scaffoldar React + Vite + Tailwind.
DECISAO: (b). O `AGENTS.md` ja fixa React + TS + Vite + Tailwind como stack; comecar em HTML criaria retrabalho de migracao.
DECISAO DE CONTEUDO: estrutura e padroes de UI foram usados como referencia, mas marca, copy e depoimentos da pagina original nao foram copiados - o texto foi escrito a partir do proprio `IA.md` (3 perfis, OpenRouter, creditos, memoria persistente).
VALIDACAO: `npm run build` compilou (tsc + vite, 31 modulos, 0 erro); `npm run lint` (oxlint) sem apontamentos; dev server respondeu HTTP 200 com o `<title>` correto; copy das 7 secoes e tokens de cor conferidos no bundle de producao; `start_app.py` executado (status, opcao invalida e saida).

## Testes importantes

[2026-07-28] Sem teste automatizado ainda. A landing e UI puramente visual e sem regra de negocio, caso em que o `GUIA_MINIMO_QUALIDADE.md` (item 7, "regua unica de testes") aceita verificacao manual registrada. Testes automatizados passam a ser obrigatorios quando entrar logica de negocio (autenticacao, creditos, gateway de IA).

Verificacao manual executada em 2026-07-28:

| Verificacao | Comando | Resultado |
|-------------|---------|-----------|
| Compilacao TS + bundle | `npm run build` | 31 modulos, 0 erro, ~228ms |
| Lint | `npm run lint` (oxlint) | sem apontamentos |
| Servidor de dev | `npm run dev` + `curl` | HTTP 200, `<title>` correto |
| Copy das 7 secoes | grep no bundle de producao | todas presentes |
| Tokens de cor | grep no CSS de producao | presentes (ver observacao abaixo) |
| Menu de entrada | `python start_app.py` | status, opcao invalida e saida ok |

Observacao: `--color-erro` nao aparece no CSS compilado porque o Tailwind 4 so emite token efetivamente usado, e a landing nao tem estado de erro. O token segue definido em `index.css` e sera emitido quando um formulario usar. Nao e defeito.

Pendente de verificacao manual: renderizacao em navegador real (mobile e desktop) e navegacao por teclado ponta a ponta. O HTML foi construido com foco visivel, `aria-label` no menu, `aria-pressed` nas abas do demo e skip link, mas isso ainda nao foi conferido com leitor de tela.

[2026-07-28, segunda rodada] Apos identidade visual, animacoes e reestruturacao:

| Verificacao | Comando | Resultado |
|-------------|---------|-----------|
| Compilacao TS + bundle | `npm run build` | 439 modulos, 0 erro |
| Lint | `npm run lint` (oxlint) | sem apontamentos |
| Contraste WCAG dos acentos | script sobre os pares reais de cor | ver registro datado acima |
| Paleta e fontes no CSS de producao | grep no bundle | 8 hex e 2 familias presentes |
| Acentuacao no bundle | grep + varredura de mojibake | integra, sem corrupcao |

Nao verificado nesta sessao: FPS das animacoes, comportamento em telas pequenas e leitor de tela. Nao havia navegador disponivel no ambiente - os ajustes de desempenho atacam causas conhecidas de travamento, mas a confirmacao depende de execucao real.

## Bugs e fixes relevantes

_Nenhum ainda._

## Integracoes e servicos externos

- Servico: **OpenRouter** (planejada)
- Como esta configurado: ainda nao configurado
- Onde ficam variaveis: variavel de ambiente server-side, fora do repositorio
- Observacao de seguranca: chave unica da plataforma, nunca no frontend nem versionada

## Pendencias

- [ ] Definir se `Estudo-com-IA` continua como repositorio de concepcao ou se a documentacao migra para ca.
- [x] ~~Fase 0: frontend React com `start_app.py`~~ - landing entregue em 2026-07-28.
- [ ] **Publicar os mockups do `Estudo-com-IA`** (ex.: GitHub Pages apontando para `mockup/`) e preencher `BASE_DESTINOS` em `frontend/src/content/destinos.ts`. Ate la os cartoes de perfil ficam desabilitados.
- [ ] Fase 0: backend Django + login dos 3 perfis (**escopo do Felipe**). Contrato sugerido: `POST /api/auth/login` devolvendo token e perfil; o frontend passa a rotear pelo perfil autenticado em vez da escolha manual atual.
- [ ] Conferir FPS real das animacoes em navegador, sobretudo em maquina modesta.
- [ ] Fase 1: gateway OpenRouter + modulo de creditos + primeira ferramenta de IA.
- [ ] Definir estrategia de testes e comando de validacao objetiva.
- [ ] Substituir os depoimentos placeholder por relatos reais coletados na instituicao.
- [ ] Ligar os CTAs (`#comecar`, `#entrar`) as telas reais quando a autenticacao existir.
- [ ] Ligar o demo do motor de refracao ao gateway de IA (hoje e estatico e ilustrativo).
- [ ] Preencher as paginas legais do rodape (privacidade, termos, seguranca). Como a plataforma trata dados de alunos, ha dever de LGPD - ver `templates/PRIVACIDADE-LGPD-template.md` no Doktor.
- [ ] Conferir a landing em navegador real (mobile/desktop) e navegacao por teclado.

## Resumos de decisao

Use quando houver decisao complexa:

```text
[YYYY-MM-DD] CONTEXTO:
ALTERNATIVAS:
DECISAO:
VALIDACAO:
```

Nao registre chain of thought interno. Registre apenas informacao tecnica util, verificavel e retomavel.

Nao apague nem reescreva registros antigos ao mudar uma decisao: adicione um novo registro datado explicando a mudanca, o motivo e a validacao. A unica secao reescrevivel e "Estado atual (resumo vivo)".

Quando este arquivo crescer demais, mova os registros mais antigos (sem editar) para `docs/ia-archive/IA-ARCHIVE-<ano>.md` e deixe um ponteiro datado aqui.
