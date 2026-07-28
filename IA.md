# IA.md - Contexto Operacional

## Estado atual (resumo vivo)

<!--
  EXCECAO a regra append-only desta secao: ela e um RESUMO reescrevivel.
  Responde "onde o projeto esta AGORA" em poucas linhas, para retomar contexto
  sem reler toda a linha do tempo abaixo. Reescreva-a a cada mudanca de estado.
-->

[2026-07-28] Repositorio recem-criado, sem codigo de aplicacao. Padroes Doktor sincronizados em `doktor SystemDesign/`, `AGENTS.md` e `IA.md` criados. Proximo passo: Fase 0 - fundacao do monorepo (backend Django + frontend React) com `start_app.py` e login dos 3 perfis.

## Objetivo do projeto

[2026-07-28] Implementacao web do produto concebido em `Estudo-com-IA`: plataforma SaaS de estudos para instituicoes de ensino usando **OpenRouter como motor de IA**. A instituicao assina, recebe creditos de IA, e o diretor distribui para professores (gerar/corrigir provas e material) e alunos (tutor com memoria persistente). Tres perfis de login: aluno, professor, diretor.

O repositorio `Estudo-com-IA` mantem a documentacao de concepcao (visao, arquitetura, perfis, creditos, memoria, roadmap) e um mockup HTML estatico. Este repositorio contem o codigo real.

## Estado atual

- **Implementado**: nada de aplicacao ainda.
- **Em progresso**: setup inicial do repositorio.
- **Pendente**: toda a Fase 0 do roadmap.

## Stack e dependencias

- Frontend: React + TypeScript + Vite + Tailwind
- Backend: Django + Django REST Framework (monolito modular)
- Banco: PostgreSQL
- IA: OpenRouter (API unificada multi-modelo)
- Deploy: Railway
- Testes: a definir na Fase 0

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

## Testes importantes

_Nenhum ainda - sem codigo de aplicacao._

## Bugs e fixes relevantes

_Nenhum ainda._

## Integracoes e servicos externos

- Servico: **OpenRouter** (planejada)
- Como esta configurado: ainda nao configurado
- Onde ficam variaveis: variavel de ambiente server-side, fora do repositorio
- Observacao de seguranca: chave unica da plataforma, nunca no frontend nem versionada

## Pendencias

- [ ] Definir se `Estudo-com-IA` continua como repositorio de concepcao ou se a documentacao migra para ca.
- [ ] Fase 0: fundacao do monorepo (backend Django + frontend React) com `start_app.py` e login dos 3 perfis.
- [ ] Fase 1: gateway OpenRouter + modulo de creditos + primeira ferramenta de IA.
- [ ] Definir estrategia de testes e comando de validacao objetiva.

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
