#!/usr/bin/env python3
"""Menu de entrada do Prisma.

Porta unica por onde a pessoa instala, roda e valida o projeto, conforme
`doktor SystemDesign/core/GUIA-START-APP-SCRIPT.md`.

Uso:
    python start_app.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FRONTEND = RAIZ / "frontend"

# Cores ANSI. Desligadas quando o terminal nao suporta ou NO_COLOR esta setado.
_COLORIDO = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _cor(texto: str, codigo: str) -> str:
    return f"\033[{codigo}m{texto}\033[0m" if _COLORIDO else texto


def titulo(texto: str) -> str:
    return _cor(texto, "1;36")


def ok(texto: str) -> str:
    return _cor(texto, "32")


def alerta(texto: str) -> str:
    return _cor(texto, "33")


def erro(texto: str) -> str:
    return _cor(texto, "31")


def suave(texto: str) -> str:
    return _cor(texto, "90")


def npm() -> str | None:
    """Retorna o executavel do npm, ou None se nao estiver instalado.

    No Windows o npm e um .cmd, por isso a busca usa shutil.which em vez de
    assumir o nome puro.
    """
    return shutil.which("npm")


def rodar(args: list[str], cwd: Path) -> int:
    """Executa um comando mostrando a saida em tempo real."""
    executavel = npm()
    if executavel is None:
        print(erro("\n  npm nao encontrado no PATH."))
        print("  Instale o Node.js 20+ em https://nodejs.org e tente de novo.\n")
        return 1

    print(suave(f"\n  > npm {' '.join(args)}  ({cwd.name})\n"))
    try:
        return subprocess.call([executavel, *args], cwd=cwd)
    except KeyboardInterrupt:
        print(suave("\n  Interrompido.\n"))
        return 130
    except OSError as exc:
        print(erro(f"\n  Falha ao executar npm: {exc}\n"))
        return 1


def dependencias_instaladas() -> bool:
    return (FRONTEND / "node_modules").is_dir()


def acao_instalar() -> None:
    print(titulo("\n  Instalando dependencias do frontend"))
    if rodar(["install"], FRONTEND) == 0:
        print(ok("\n  Dependencias instaladas.\n"))
    else:
        print(erro("\n  A instalacao falhou. Veja a saida acima.\n"))


def acao_rodar() -> None:
    if not dependencias_instaladas():
        print(alerta("\n  Dependencias ausentes. Rodando a instalacao primeiro."))
        if rodar(["install"], FRONTEND) != 0:
            print(erro("\n  Nao foi possivel instalar. Abortando.\n"))
            return

    print(titulo("\n  Servidor de desenvolvimento"))
    print(suave("  Encerre com Ctrl+C.\n"))
    rodar(["run", "dev"], FRONTEND)


def acao_build() -> None:
    if not dependencias_instaladas():
        print(alerta("\n  Instale as dependencias antes (opcao 2).\n"))
        return

    print(titulo("\n  Build de producao"))
    if rodar(["run", "build"], FRONTEND) == 0:
        print(ok("\n  Build concluido em frontend/dist.\n"))
    else:
        print(erro("\n  O build falhou. Veja a saida acima.\n"))


def acao_validar() -> None:
    if not dependencias_instaladas():
        print(alerta("\n  Instale as dependencias antes (opcao 2).\n"))
        return

    print(titulo("\n  Validacao: lint + build"))
    if rodar(["run", "lint"], FRONTEND) != 0:
        print(erro("\n  Lint reprovou.\n"))
        return
    print(ok("  Lint aprovado."))

    if rodar(["run", "build"], FRONTEND) != 0:
        print(erro("\n  Build reprovou.\n"))
        return
    print(ok("\n  Validacao concluida: lint e build aprovados.\n"))


def acao_status() -> None:
    print(titulo("\n  Status do ambiente\n"))

    versao_npm = "nao encontrado"
    executavel = npm()
    if executavel:
        try:
            versao_npm = subprocess.run(
                [executavel, "--version"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            ).stdout.strip() or "desconhecida"
        except (OSError, subprocess.SubprocessError):
            versao_npm = "falha ao consultar"

    linhas = [
        ("Python", sys.version.split()[0]),
        ("npm", versao_npm),
        ("Pasta frontend", "ok" if FRONTEND.is_dir() else "ausente"),
        ("Dependencias", "instaladas" if dependencias_instaladas() else "ausentes"),
        ("Build anterior", "sim" if (FRONTEND / "dist").is_dir() else "nao"),
    ]

    for rotulo, valor in linhas:
        marcador = ok("*") if valor not in {"ausente", "ausentes", "nao encontrado"} else alerta("!")
        print(f"   {marcador} {rotulo:<16} {valor}")

    print()


OPCOES = {
    "1": ("Rodar o site (dev)", acao_rodar),
    "2": ("Instalar dependencias", acao_instalar),
    "3": ("Gerar build de producao", acao_build),
    "4": ("Validar (lint + build)", acao_validar),
    "5": ("Status do ambiente", acao_status),
}


def menu() -> None:
    print(titulo("\n  PRISMA"))
    print(suave("  Plataforma de estudos com IA para instituicoes de ensino\n"))

    for chave, (rotulo, _) in OPCOES.items():
        print(f"   {titulo(chave)}  {rotulo}")
    print(f"   {titulo('0')}  Sair\n")


def main() -> int:
    if not FRONTEND.is_dir():
        print(erro(f"\n  Pasta frontend nao encontrada em {FRONTEND}\n"))
        return 1

    while True:
        menu()
        try:
            escolha = input("  Escolha uma opcao: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(suave("\n  Ate mais.\n"))
            return 0

        if escolha == "0":
            print(suave("\n  Ate mais.\n"))
            return 0

        entrada = OPCOES.get(escolha)
        if entrada is None:
            print(alerta("\n  Opcao invalida. Escolha um numero do menu.\n"))
            continue

        entrada[1]()


if __name__ == "__main__":
    raise SystemExit(main())
