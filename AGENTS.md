# AGENTS.md - Roteiro de IA do Projeto

> **O que e**: Arquivo raiz para orientar agentes de IA neste projeto.
>
> **Objetivo**: Manter a IA direcionada, preservar qualidade minima e reduzir consumo de contexto. A IA deve ler o minimo necessario para a tarefa, sem abrir documentacao "por garantia".

---

## 0. Contexto deste projeto

O **PrismaTest** e a implementacao web do produto documentado em `Estudo-com-IA`: uma plataforma SaaS de estudos para instituicoes de ensino, com OpenRouter como motor de IA, creditos por assinatura e memoria persistente por aluno.

O repositorio de origem contem a concepcao (visao, arquitetura, perfis, creditos, memoria, roadmap) e um mockup HTML estatico. Este repositorio contem o **codigo real**.

Os padroes de qualidade ficam sincronizados em `doktor SystemDesign/`, atualizaveis com o comando `doktor` rodado na raiz.

## 1. Principio central

Este arquivo nao e um framework rigido. Ele e um roteador leve:

- define o contrato minimo antes de qualquer entrega;
- aponta quais documentos abrir por tipo de tarefa;
- evita reler guias grandes sem necessidade;
- registra onde a IA deve atualizar contexto, decisoes e validacoes.

## 2. Leitura obrigatoria

1. Leia sempre `doktor SystemDesign/core/GUIA_MINIMO_QUALIDADE.md`.
2. Antes de alterar arquivos, leia `IA.md` - comece pela secao "Estado atual (resumo vivo)", nao pelo historico completo.
3. Use `README.md` para entender setup, comandos e objetivo publico.
4. Depois disso, abra apenas os documentos indicados na secao 3. Uma tarefa comum precisa de no maximo 1-2 documentos alem do guia minimo. Ter mais guias opcionais disponiveis no acervo nao significa ler mais - abra no maximo 1 guia opcional por tarefa.
5. Antes de editar manualmente, procure automacao existente (script, comando, instalador). Reutilize ou estenda antes de editar na mao; se editar manualmente, registre o motivo.

## 3. Roteiro por tipo de tarefa

Todos os caminhos abaixo sao relativos a `doktor SystemDesign/`.

| Se a tarefa e... | Leia alem do guia minimo |
|------------------|--------------------------|
| Frontend, UI ou UX | `core/DESIGN_SYSTEM_FRONTEND.md` |
| Backend, API, banco ou regra de negocio | `core/DESIGN_SYSTEM_BACKEND.md` |
| API REST, contratos ou status codes | `core/DESIGN_SYSTEM_API_REST.md` |
| Estrutura, camadas ou organizacao de codigo | `core/DESIGN_SYSTEM_ARQUITETURA.md` |
| Seguranca, secrets, auth ou dados sensiveis | `core/DESIGN_SYSTEM_SEGURANCA.md` |
| Testes, cobertura, mocks ou nomenclatura | `core/DESIGN_SYSTEM_TESTES.md` |
| README ou documentacao | `core/DESIGN_SYSTEM_README.md` |
| Stack, arquitetura ou decisao tecnica | `docs/STACK-E-ARQUITETURA.md` |
| Qualquer programa rodavel (web, CLI, automacao, script) | `core/GUIA-START-APP-SCRIPT.md` |
| Qual nivel de IA usar ou como economizar contexto | `core/DESIGN_SYSTEM_ECONOMIA_IA.md` |
| Chamada de LLM, agente ou gateway de IA | `guias/integracao/GUIA-INTEGRACAO-LLM-E-AGENTES.md` |
| Login por token, JWT ou OAuth | `guias/backend/GUIA-AUTENTICACAO-JWT-OAUTH.md` |
| Deploy no Railway | `guias/integracao/GUIA-DEPLOY-RAILWAY.md` |
| Validar projeto pronto | `docs/CHECKLIST-PROJETO-PRONTO.md` |
| Funcionalidade especifica | Guia opcional correspondente, somente se existir e casar com a tarefa |

## 4. Arquivo pequeno e de responsabilidade unica

**Regra: um arquivo, um assunto.** Nada de arquivao que junta tudo.

O motivo e economico, nao estetico. Para trocar a cor de um botao num
arquivo de 1700 linhas, a IA le 1700 linhas - gasta tempo, gasta token e
ainda arrisca mexer no que nao devia. Se o botao mora num arquivo de 60
linhas, ela le 60. **Arquivo pequeno e o que torna conserto barato.**

### Limites praticos

| Tipo | Alvo | Limite |
|------|------|--------|
| Componente React (`.tsx`) | ate 150 linhas | 200 |
| Modulo Python | ate 200 linhas | 300 |
| Modulo de estilo, config ou conteudo | ate 200 linhas | 300 |
| Documento em `docs/` | ate 250 linhas | 400 |

Passou do limite: quebre. Nao sao numeros sagrados - um arquivo coeso de
220 linhas e melhor que tres picotados de 70 sem sentido proprio. Mas
passar do limite e o **sinal de parar e perguntar** se ainda ha um so
assunto ali dentro.

### Como quebrar

Separe por **responsabilidade**, nao por tamanho. Cada pedaco deve poder
ser nomeado numa frase curta sem "e":

- `Header.tsx` faz o cabecalho. Bom.
- `utils.tsx` faz "varias coisas uteis". Ruim - vira deposito.

Onde cada coisa vive neste projeto:

| O que e | Onde vai |
|---------|----------|
| Componente base reutilizavel | `frontend/src/components/ui/` |
| Estrutura de pagina | `frontend/src/components/layout/` |
| Secao com regra propria | `frontend/src/components/feature/` |
| Texto, copy, links | `frontend/src/content/` |
| Token de design, cor, fonte | `frontend/src/index.css` (`@theme`) |
| Automacao | `scripts/`, um arquivo por tarefa |

**Texto nunca fica dentro do componente.** Copy vive em
`frontend/src/content/` - editar uma frase nao pode exigir abrir JSX.

### Debitos conhecidos

Registrados porque ja existem e violam a regra. Ao mexer neles, **quebre
antes** em vez de aumentar:

- `start_app.py` (1716 linhas) - HUD Tkinter com janela, estado, console
  e acoes num arquivo so. Ao mexer, extraia para `scripts/hud/` por
  responsabilidade (layout, console, acoes, estado do ambiente).
- `IA.md` (350 linhas) - crescimento e esperado, e append-only. Quando
  passar de ~400, mova os registros antigos **sem editar** para
  `docs/ia-archive/IA-ARCHIVE-<ano>.md` e deixe um ponteiro datado.
  Nunca apague.

Nao quebre esses dois "de passagem" numa tarefa que nao os envolve: e
mudanca estrutural, merece commit proprio.

## 5. Regras praticas

- Nao leia documentos por garantia.
- Nao invente stack: este projeto ja definiu React + TypeScript + Vite + Tailwind no frontend e Django + DRF + PostgreSQL no backend.
- Ao mudar comportamento, comandos, estrutura ou decisao, atualize `README.md`, `IA.md` ou `docs/` no mesmo passo, em tempo real (nao deixe para o fim do trabalho).
- O `IA.md` e linha do tempo: nao apague registros antigos ao mudar uma decisao; adicione um novo registro datado com motivo e validacao.
- Todo programa rodavel entrega `start_app.py` na raiz como porta de entrada unica - nao flags de linha de comando. **Neste projeto o `start_app.py` e uma janela grafica (Tkinter), nao um menu de terminal**: desvio consciente do guia do Doktor, registrado em `IA.md` (2026-07-29). Nao "corrija" de volta para menu de terminal sem decisao explicita do Andre.
- Antes de usar uma API, biblioteca ou metodo, confirme que ela existe na versao instalada - nao presuma de memoria.
- Registre validacao objetiva com evidencia real de execucao: comando de teste rodado e saida observada, checklist manual, ou motivo de nao haver teste automatico. "Deve funcionar" nao e validacao.
- Prefira automacao a edicao manual quando ja existir script ou ferramenta reutilizavel para a mudanca.
- Ao versionar, use Conventional Commits: `tipo(escopo): descricao no imperativo`. Tipos validos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`. Cada commit e uma unidade coesa e separada - nao misture temas diferentes no mesmo commit.
- **A chave do OpenRouter e server-side e vive em variavel de ambiente.** Nunca no frontend, nunca no repositorio. Toda chamada de IA passa pelo gateway do backend.
- Nunca exponha segredo, token, dado pessoal ou caminho local privado em documentacao publica.

## 6. Criterio de pronto

Uma entrega so esta pronta quando outra pessoa ou outra IA consegue entender:

- o que mudou;
- por que mudou;
- como rodar;
- como validar;
- qual risco ou limite ainda existe.

E quando a mudanca **nao deixou nenhum arquivo maior que o limite da
secao 4** sem registro explicito do motivo.
