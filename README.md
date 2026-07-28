# PrismaTest

Implementacao web da plataforma de estudos com IA para instituicoes de ensino: OpenRouter como motor de IA, creditos por assinatura e memoria persistente por aluno.

> **Status: Fase 0 - fundacao.** A landing page publica ja esta implementada. O backend ainda nao existe. A concepcao do produto (visao, arquitetura, perfis, creditos, memoria, roadmap) vive no repositorio `Estudo-com-IA`.

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
├── frontend/               # React + TypeScript + Vite + Tailwind
│   └── src/
│       ├── components/
│       │   ├── ui/         # Button, Card, Badge, Secao, Logo
│       │   ├── layout/     # Header, Rodape
│       │   └── feature/    # Secoes da landing
│       ├── content/        # Copy da landing, separada do JSX
│       └── index.css       # Tokens de design (@theme do Tailwind 4)
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
