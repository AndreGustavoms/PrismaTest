# PrismaTest

Implementacao web da plataforma de estudos com IA para instituicoes de ensino: OpenRouter como motor de IA, creditos por assinatura e memoria persistente por aluno.

> **Status: Fase 0 - fundacao.** A landing page publica esta implementada, com a identidade visual do documento UX/UI aplicada. O backend ainda nao existe. A concepcao do produto (visao, arquitetura, perfis, creditos, memoria, roadmap) e os mockups das telas por perfil vivem no repositorio [`Estudo-com-IA`](https://github.com/flaviavs-commits/Estudo-com-IA).

**Divisao de trabalho:** Andre no frontend, Felipe no backend.

## Sobre

A instituicao assina a plataforma e recebe creditos de IA, distribuidos pelo diretor entre professores e alunos:

| Perfil | Foco | Principais ferramentas |
|--------|------|------------------------|
| Aluno | Estudar | Tutor de IA com memoria, gerador de textos de estudo, simulados, notas e faltas |
| Professor | Ensinar | Geracao e correcao de provas, banco de conteudo, material didatico, lancamento de notas |
| Diretor | Administrar | Dashboards de desempenho, gestao de usuarios e turmas, distribuicao de creditos |

## Stack

| Camada | Tecnologia | Papel |
|--------|-----------|-------|
| Frontend | React + TypeScript + Vite + Tailwind | SPA com areas separadas por perfil |
| Backend | Django + Django REST Framework | API, regras de negocio, contabilidade de creditos |
| IA | OpenRouter | Acesso multi-modelo (geracao, correcao, tutoria) |
| Banco | PostgreSQL | Usuarios, conteudo, notas, faltas, creditos, memoria |
| Deploy | Railway | Hospedagem do backend |

Toda chamada de IA passa pelo gateway do backend. O frontend nunca fala com o OpenRouter diretamente.

## Estrutura

```
PrismaTest/
├── AGENTS.md               # Roteiro para agentes de IA neste projeto
├── IA.md                   # Memoria operacional: decisoes, estado e validacoes
├── README.md
├── start_app.py            # Menu de entrada: rodar, instalar, validar
├── scripts/                # Automacoes (sincronizar-app.py)
├── frontend/               # React + TypeScript + Vite + Tailwind
│   ├── public/app/         # Telas da aplicacao (copia derivada, ignorada)
│   └── src/
│       ├── components/
│       │   ├── ui/         # Base (Button, Card, Secao) e animacao
│       │   │               # (Animar, Titulo3D, Atmosfera, Card3D)
│       │   ├── layout/     # Header, Rodape
│       │   └── feature/    # Secoes da landing
│       ├── content/        # Copy e destino da aplicacao
│       └── index.css       # Tokens de design e regra de cor (@theme)
└── doktor SystemDesign/    # Padroes de qualidade (copia sincronizada, nao versionada)
```

## Como rodar

Requisitos: Node.js 20+ e Python 3.10+.

```bash
python start_app.py
```

O menu cobre instalar dependencias, rodar o site, gerar build e validar. Para rodar direto, sem o menu:

```bash
cd frontend
npm install
npm run dev
```

O site fica em `http://localhost:5173`.

## Como validar

Pela opcao 4 do `start_app.py`, ou direto:

```bash
cd frontend
npm run lint     # oxlint
npm run build    # tsc + vite build
```

Ainda nao ha teste automatizado: a landing e UI visual sem regra de negocio, caso em que o guia minimo de qualidade aceita verificacao manual registrada. As verificacoes executadas estao em [IA.md](IA.md), secao "Testes importantes". Testes automatizados entram junto com a logica de negocio (autenticacao, creditos, gateway de IA).

## Landing e aplicacao

Sao duas coisas, em repositorios diferentes:

| | Onde vive | O que e |
|---|---|---|
| **Landing** | este repositorio, `frontend/src/` | vitrine publica, em React |
| **Aplicacao** | `Estudo-com-IA`, pasta `mockup/` | telas de aluno, professor e diretor |

Ao clicar em "Entrar", a landing abre a tela inicial da aplicacao,
que faz a escolha de perfil.

### Sincronizar a aplicacao

As telas sao mantidas no `Estudo-com-IA`. Para trazer a versao atual:

```bash
python scripts/sincronizar-app.py
```

Isso copia as telas para `frontend/public/app/`, que o Vite serve em
`/app/`. **Rode de novo sempre que as telas mudarem la** - a pasta e
uma copia derivada, ignorada pelo git.

O script tambem ajusta o link interno `landing.html`, que nao existe
mais aqui, para a raiz do site.

> **Nao ha autenticacao.** Qualquer pessoa acessa qualquer area: o
> "Entrar" e navegacao, nao controle de acesso. O login real entra
> com o backend. Quando existir, basta trocar `ENTRADA_APP` em
> `frontend/src/content/destinos.ts` - todos os botoes leem de la.

## Personalizar a landing

O texto fica em `frontend/src/content/landing.ts`, separado dos componentes. As cores e a tipografia ficam em `frontend/src/index.css`, no bloco `@theme`.

Os depoimentos sao **placeholders propositais**, com borda tracejada. Substitua por relatos reais antes de publicar.

## Padroes de qualidade

Este projeto segue o [Doktor System-Design](https://github.com/AndreGustavoms/Doktor-SystemDesign). Os padroes ficam em `doktor SystemDesign/`, uma copia sincronizada e **nao versionada** (esta no `.gitignore`).

Para trazer ou atualizar essa pasta:

```powershell
doktor
```

Se o comando nao existir, instale-o uma vez:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<caminho-do-Doktor>\scripts\powershell\install-doktor-powershell.ps1"
```

Mudancas nos padroes vao no repositorio Doktor System-Design, nunca nesta copia local.

## Licenca

A definir.
