#!/usr/bin/env python3
"""HUD de entrada do Prisma.

Porta unica por onde a pessoa instala, roda e valida o projeto. Abre uma
janela (Tkinter) com o estado do ambiente ao vivo e as acoes em cards.

DESVIO REGISTRADO
    O `doktor SystemDesign/core/GUIA-START-APP-SCRIPT.md` pede um menu
    interativo *no terminal* (questionary/rich). Este projeto usa uma
    janela grafica no lugar, por decisao do Andre (2026-07-29). O motivo
    e o publico: a landing e um produto visual, e quem roda isso esta
    numa maquina com display.

    Consequencia aceita: nao ha porta de entrada em ambiente sem display
    (SSH, container, CI). Nesses casos, use os comandos direto:

        cd frontend && npm install
        cd frontend && npm run dev
        cd frontend && npm run lint && npm run build

    Ver IA.md, secao de decisoes.

NOTA DE IMPLEMENTACAO VISUAL
    O Tk 8.6 nao tem canto arredondado, sombra nem transicao em widget
    nativo. Os cards sao portanto DESENHADOS em Canvas: o arredondado sai
    de um poligono suavizado (`smooth=True`), a "sombra" de um contorno
    mais claro deslocado, e a animacao de hover de uma interpolacao de
    cor por `after`. Trocar isso por `tk.Button` devolve o visual de
    formulario antigo - foi justamente o que este desenho substituiu.

Uso:
    python start_app.py
"""

from __future__ import annotations

import queue
import re
import shutil
import socket
import subprocess
import sys
import threading
import webbrowser
from functools import lru_cache
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import font as tkfont
except ImportError:  # pragma: no cover - depende da instalacao do Python
    print("Tkinter nao esta disponivel nesta instalacao do Python.")
    print("No Windows, reinstale o Python marcando 'tcl/tk and IDLE'.")
    raise SystemExit(1) from None

RAIZ = Path(__file__).resolve().parent
FRONTEND = RAIZ / "frontend"
SINCRONIZAR_APP = RAIZ / "scripts" / "sincronizar-app.py"

PORTA_PADRAO = 5173

# O npm e o Vite colorem a saida com escapes ANSI. No terminal isso vira
# cor; no widget de texto do Tk vira lixo visivel ("<-[32m"). Como o
# console ja tem cor propria por tag, os escapes saem na entrada.
ESCAPES_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def limpar_ansi(texto: str) -> str:
    """Tira os codigos de cor ANSI de uma linha de saida."""
    return ESCAPES_ANSI.sub("", texto)


# Como os subprocessos sao abertos, em um lugar so.
#   - encoding/errors: o npm imprime caracteres que o console cp1252 do
#     Windows nao aceita; sem isso a leitura estoura.
#   - CREATE_NO_WINDOW: evita um console piscando ao lado da janela.
SAIDA_SUBPROCESSO: dict[str, object] = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.STDOUT,
    "text": True,
    "encoding": "utf-8",
    "errors": "replace",
    "creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0),
}

# O mesmo, mas em bytes: o console interativo decodifica por conta.
# Ferramentas modernas (npm, git, node) escrevem UTF-8, mas o proprio
# `cmd.exe` responde no codepage OEM (cp850 em portugues) - decodificar
# tudo como UTF-8 transforma "operável" em "oper?vel". Ver `decodificar`.
SAIDA_BYTES: dict[str, object] = {
    "stdout": subprocess.PIPE,
    "stderr": subprocess.STDOUT,
    "creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0),
}

# Codepage que o shell usa nas mensagens dele. `getpreferredencoding`
# devolve o ANSI (cp1252), que nao serve: o que sai do pipe e o OEM.
def _codepage_oem() -> str:
    if sys.platform != "win32":
        return "utf-8"
    try:
        import ctypes

        return f"cp{ctypes.windll.kernel32.GetOEMCP()}"
    except Exception:  # noqa: BLE001 - sem codepage, o padrao resolve
        return "cp850"


CODEPAGE_SHELL = _codepage_oem()


def decodificar(bruto: bytes) -> str:
    """Decodifica uma linha de saida tentando UTF-8 e caindo no OEM.

    UTF-8 primeiro porque e o que as ferramentas do projeto usam; o
    codepage do console entra so quando a linha nao e UTF-8 valido, que
    e o caso das mensagens do proprio `cmd.exe`.
    """
    try:
        return bruto.decode("utf-8")
    except UnicodeDecodeError:
        return bruto.decode(CODEPAGE_SHELL, errors="replace")

# ---------------------------------------------------------------------
# Design tokens
#
# A paleta vem de frontend/src/index.css (@theme) - o HUD e a landing
# sao o mesmo produto. O console foge disso de proposito: terminal
# escuro e a convencao que a pessoa ja reconhece.
# ---------------------------------------------------------------------

FUNDO = "#f7f5ee"          # creme da landing
SUPERFICIE = "#fffdf8"     # cards
SUPERFICIE_HOVER = "#fbf9f2"
SUPERFICIE_ALT = "#f0ece1"  # hover do botao secundario, um degrau mais forte
BORDA = "#e8e2d4"          # divisoria suave, nunca linha forte
BORDA_HOVER = "#d5cfc0"
SOMBRA = "#efeade"         # "sombra": contorno claro deslocado

TEXTO = "#1a1a1a"          # grafite
TEXTO_SUAVE = "#6b6862"
TEXTO_TENUE = "#6f6b63"

MARCA = "#c85a3c"          # terracota
MARCA_ESCURA = "#a8482f"

SUCESSO = "#356e45"
SUCESSO_FUNDO = "#e6efe6"
ALERTA = "#8a6015"
ALERTA_FUNDO = "#f7efdc"
ERRO = "#b83c2e"
ERRO_FUNDO = "#f7e4e0"
INFO = "#3f5f8e"
INFO_FUNDO = "#e4ebf5"

CONSOLE_FUNDO = "#151515"
CONSOLE_ENTRADA = "#1e1e1e"   # linha de comando, um degrau acima do fundo
CONSOLE_TEXTO = "#a8d5a8"
CONSOLE_SUAVE = "#8a8a8a"
CONSOLE_ERRO = "#e0796b"
CONSOLE_OK = "#7fc98a"
CONSOLE_COMANDO = "#e8c17a"   # eco do que a pessoa digitou
CONSOLE_BARRA = "#3a3a3a"
CONSOLE_BARRA_ATIVA = "#5a5a5a"

# `Inter` e a fonte da landing, mas raramente esta instalada no Windows.
# `Segoe UI` e a substituta mais proxima em metrica e desenho.
FAMILIA = "Inter"
FAMILIA_MONO = "Cascadia Code"

# Icones: a fonte nativa do Windows 11 desenha simbolos geometricos que
# herdam a cor do texto. Emoji colorido nao herda cor - ficaria com o
# mesmo tom no card escuro e no claro, e destoaria da paleta.
FAMILIA_ICONE = "Segoe Fluent Icons"

# Pontos de codigo da Segoe Fluent Icons usados nos cards.
ICONES = {
    "rodar": "",       # play
    "parar": "",       # stop
    "navegador": "",   # globo
    "pacote": "",      # caixa
    "sincronizar": "", # sync
    "build": "",       # blocos
    "validar": "",     # check
    "porta": "",       # engrenagem
    "limpar": "",      # lixeira
}

RAIO = 14                  # bordas suaves, 12-16px como pedido
ESPACO = 20                # respiro entre secoes
ALTURA_CONSOLE = 300       # piso do console, para caber saida de verdade


def fonte_disponivel(raiz: tk.Misc, preferida: str, reserva: str) -> str:
    """Devolve `preferida` se instalada, senao `reserva`."""
    return preferida if preferida in set(tkfont.families(raiz)) else reserva


def misturar(cor_a: str, cor_b: str, fracao: float) -> str:
    """Interpola duas cores hex. Usado nas transicoes de hover."""
    a = tuple(int(cor_a[i : i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(cor_b[i : i + 2], 16) for i in (1, 3, 5))
    c = tuple(round(x + (y - x) * fracao) for x, y in zip(a, b))
    return f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}"


def retangulo_redondo(
    canvas: tk.Canvas, x1: float, y1: float, x2: float, y2: float, raio: float, **kw
) -> int:
    """Desenha um retangulo de cantos arredondados.

    O Tk nao tem primitiva para isso. O contorno e um poligono cujos
    cantos repetem pontos; `smooth=True` transforma essa repeticao na
    curva. E a unica forma de ter canto redondo real em Canvas.
    """
    pontos = [
        x1 + raio, y1,
        x2 - raio, y1,
        x2, y1,
        x2, y1 + raio,
        x2, y2 - raio,
        x2, y2,
        x2 - raio, y2,
        x1 + raio, y2,
        x1, y2,
        x1, y2 - raio,
        x1, y1 + raio,
        x1, y1,
    ]
    return canvas.create_polygon(pontos, smooth=True, splinesteps=16, **kw)


# Pontos do triangulo do prisma-logo-minimal.svg, convertidos do viewBox
# original (1254x1254). Mantidos em um so lugar para as tres aplicacoes
# (HUD, favicon, landing) desenharem a mesma forma exata.
LOGO_TOPO = (16.0, 6.38)
LOGO_ESQ = (6.35, 21.56)
LOGO_DIR = (25.65, 21.56)
LOGO_BASE = (16.0, 25.37)
LOGO_MEIO = (16.0, 17.51)

# Recorte nos limites reais do desenho (x: 6.35-25.65, y: 6.38-25.37),
# com margem simetrica de 1.2 - o mesmo viewBox usado em Logo.tsx e no
# favicon. Um enquadramento maior que o desenho (ex.: 0-32 inteiro) deixa
# folga desigual acima/abaixo do traco; ao lado de texto em caixa alta
# (sem descendentes), essa folga fazia o triangulo parecer flutuar acima
# da linha do texto em vez de alinhado com ele.
_LOGO_ORIGEM = (5.15, 5.18)
_LOGO_DIMENSAO = (21.8, 21.39)


def desenhar_logo_prisma(canvas: tk.Canvas, cor: str, tamanho: float = 30) -> None:
    """Desenha a marca do Prisma num Canvas quadrado de `tamanho` px."""
    escala = tamanho / max(_LOGO_DIMENSAO)

    def p(ponto: tuple[float, float]) -> tuple[float, float]:
        return (
            (ponto[0] - _LOGO_ORIGEM[0]) * escala,
            (ponto[1] - _LOGO_ORIGEM[1]) * escala,
        )

    topo, esq, dire, base, meio = (
        p(LOGO_TOPO), p(LOGO_ESQ), p(LOGO_DIR), p(LOGO_BASE), p(LOGO_MEIO)
    )
    largura_traco = max(1, round(1.6 * escala))
    kw = {"fill": cor, "width": largura_traco, "capstyle": "round", "joinstyle": "round"}

    canvas.create_line(*topo, *esq, *base, *dire, *topo, **kw)
    canvas.create_line(*topo, *base, **kw)
    canvas.create_line(*esq, *meio, *dire, **kw)


def npm() -> str | None:
    """Retorna o executavel do npm, ou None se nao estiver no PATH."""
    return _npm_cacheado()


@lru_cache(maxsize=1)
def _npm_cacheado() -> str | None:
    """No Windows o npm e um .cmd, por isso shutil.which.

    Cacheado: o status consulta isso a cada ciclo, e o npm nao aparece
    nem some no meio da sessao.
    """
    return shutil.which("npm")


def dependencias_instaladas() -> bool:
    return (FRONTEND / "node_modules").is_dir()


def app_sincronizada() -> bool:
    """Diz se as telas da aplicacao ja foram trazidas para ca."""
    return (FRONTEND / "public" / "app" / "index.html").is_file()


def porta_em_uso(porta: int) -> bool:
    """Diz se ja ha algo escutando na porta.

    IPv6 vem primeiro de proposito. No Windows, conectar numa porta sem
    listener nao leva RST rapido: gasta o timeout inteiro. Como o Vite
    escuta em `::1`, testar v6 antes resolve o caso comum (servidor no
    ar) em poucos milissegundos, em vez de ~420 ms.

    Com a porta livre, porem, as duas familias gastam o timeout - por
    isso o timeout e curto e quem chama de forma repetida usa uma
    thread (ver `Hud._agendar_status`), nunca o laco do Tkinter.
    """
    for familia, endereco in ((socket.AF_INET6, "::1"), (socket.AF_INET, "127.0.0.1")):
        try:
            with socket.socket(familia, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.25)
                if sock.connect_ex((endereco, porta)) == 0:
                    return True
        except OSError:
            continue
    return False


def encerrar_arvore(processo: subprocess.Popen) -> None:
    """Encerra o processo e os filhos dele.

    O `npm run dev` e um wrapper: quem abre a porta e um `node` neto. No
    Windows, `terminate()` mata so o wrapper e deixa o Vite orfao ainda
    segurando a porta - o HUD diria "parado" com o site no ar. Por isso o
    encerramento vai pela arvore inteira (`taskkill /T`).
    """
    if processo.poll() is not None:
        return

    if sys.platform == "win32":
        try:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(processo.pid)],
                capture_output=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            processo.kill()
    else:
        processo.terminate()

    try:
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        processo.kill()


class BotaoModal:
    """Botao do modal, desenhado para combinar com os cards.

    O `tk.Button` nativo traz o relevo cinza do Windows e ignora cor de
    fundo em varios temas - o mesmo motivo que levou os cards para o
    Canvas.
    """

    ALTURA = 38

    def __init__(
        self,
        pai: tk.Widget,
        texto: str,
        callback,
        fonte: tkfont.Font,
        primario: bool = False,
        largura: int = 108,
    ) -> None:
        self.callback = callback
        self.texto = texto
        self.fonte = fonte
        self.primario = primario
        self._fracao = 0.0

        self.canvas = tk.Canvas(
            pai, width=largura, height=self.ALTURA, bg=SUPERFICIE,
            highlightthickness=0, bd=0, cursor="hand2",
        )
        self.canvas.bind("<Configure>", lambda _e: self._desenhar())
        self.canvas.bind("<Enter>", lambda _e: self._pintar(1.0))
        self.canvas.bind("<Leave>", lambda _e: self._pintar(0.0))
        self.canvas.bind("<ButtonRelease-1>", lambda _e: self.callback())

    def _pintar(self, fracao: float) -> None:
        self._fracao = fracao
        self._desenhar()

    def _desenhar(self) -> None:
        largura = self.canvas.winfo_width()
        if largura <= 1:
            return
        self.canvas.delete("all")

        if self.primario:
            fundo = misturar(TEXTO, MARCA_ESCURA, self._fracao)
            borda, cor = fundo, "#ffffff"
        else:
            fundo = misturar(SUPERFICIE, SUPERFICIE_ALT, self._fracao)
            borda, cor = BORDA_HOVER, TEXTO

        retangulo_redondo(
            self.canvas, 1, 1, largura - 1, self.ALTURA - 1, 9,
            fill=fundo, outline=borda, width=1,
        )
        self.canvas.create_text(
            largura / 2, self.ALTURA / 2, text=self.texto, font=self.fonte, fill=cor,
        )


class Modal:
    """Janela de dialogo na identidade do projeto.

    Substitui `simpledialog` e `messagebox`, que desenham o widget cru do
    Windows - fundo cinza, botao com relevo, fonte do sistema. Aqui a
    janela usa a mesma paleta, tipografia e cantos dos cards.

    Modal de verdade: `transient` + `grab_set` prendem o foco, Enter
    confirma, Esc cancela.
    """

    def __init__(
        self,
        pai: tk.Tk,
        fontes: dict[str, tkfont.Font],
        titulo: str,
        mensagem: str,
        confirmar: str = "Confirmar",
        cancelar: str = "Cancelar",
        valor_inicial: str | None = None,
        dica: str = "",
    ) -> None:
        self.resultado: str | None = None
        self.fontes = fontes
        self.tem_entrada = valor_inicial is not None

        self.janela = tk.Toplevel(pai)
        self.janela.title(titulo)
        # O fundo da janela e o tom do FUNDO da landing, nao o da
        # SUPERFICIE do cartao: e o que aparece nos 4 cantos onde o
        # retangulo arredondado deixa de cobrir - o mesmo truque dos
        # cards. Sem isso, o corte do arredondado mostraria um quadrado
        # branco atras.
        self.janela.configure(bg=FUNDO)
        self.janela.resizable(False, False)
        self.janela.transient(pai)

        # Sem barra de titulo do sistema o modal fica coerente com o
        # resto; o titulo e desenhado por nos.
        self.janela.overrideredirect(True)

        # A moldura arredondada e desenhada em Canvas, como os cards:
        # `tk.Frame` com `highlightthickness` so faz cantos retos.
        self.tela = tk.Canvas(self.janela, bg=FUNDO, highlightthickness=0, bd=0)
        self.tela.pack(fill="both", expand=True)
        self.tela.bind("<Configure>", lambda _e: self._redesenhar_moldura())

        moldura = tk.Frame(self.tela, bg=SUPERFICIE)
        self.tela.create_window(0, 0, window=moldura, anchor="nw", tags="conteudo")

        tk.Label(
            moldura, text=titulo, font=fontes["modal_titulo"],
            bg=SUPERFICIE, fg=TEXTO,
        ).pack(anchor="w", padx=26, pady=(24, 0))

        tk.Label(
            moldura, text=mensagem, font=fontes["card_desc"],
            bg=SUPERFICIE, fg=TEXTO_SUAVE, justify="left", wraplength=320,
        ).pack(anchor="w", padx=26, pady=(6, 0))

        if self.tem_entrada:
            caixa = tk.Frame(
                moldura, bg=FUNDO,
                highlightbackground=BORDA_HOVER, highlightthickness=1,
            )
            caixa.pack(fill="x", padx=26, pady=(16, 0))

            self.entrada = tk.Entry(
                caixa, font=fontes["modal_entrada"], bg=FUNDO, fg=TEXTO,
                relief="flat", bd=0, highlightthickness=0,
                insertbackground=TEXTO, justify="left",
            )
            self.entrada.pack(fill="x", padx=14, pady=11)
            self.entrada.insert(0, valor_inicial or "")
            self.entrada.select_range(0, "end")

            if dica:
                tk.Label(
                    moldura, text=dica, font=fontes["dica"],
                    bg=SUPERFICIE, fg=TEXTO_TENUE,
                ).pack(anchor="w", padx=26, pady=(7, 0))

        self.aviso = tk.Label(
            moldura, text="", font=fontes["dica"], bg=SUPERFICIE, fg=ERRO,
        )
        self.aviso.pack(anchor="w", padx=26)

        linha = tk.Frame(moldura, bg=SUPERFICIE)
        linha.pack(fill="x", padx=26, pady=(14, 22))

        # Ordem invertida: `side="right"` empilha da direita para a
        # esquerda, entao o primario e adicionado primeiro para terminar
        # na ponta direita, como manda a convencao no Windows.
        BotaoModal(
            linha, confirmar, self._confirmar, fontes["modal_botao"], primario=True
        ).canvas.pack(side="right")
        tk.Frame(linha, bg=SUPERFICIE, width=8).pack(side="right")
        BotaoModal(
            linha, cancelar, self._cancelar, fontes["modal_botao"]
        ).canvas.pack(side="right")

        self.janela.bind("<Return>", lambda _e: self._confirmar())
        self.janela.bind("<Escape>", lambda _e: self._cancelar())

        # A janela e dimensionada pelo conteudo do Frame interno, ja que
        # o Canvas nao encolhe sozinho como o Frame fazia antes.
        moldura.update_idletasks()
        largura = moldura.winfo_reqwidth()
        altura = moldura.winfo_reqheight()
        self.tela.itemconfig("conteudo", width=largura, height=altura)
        self.janela.geometry(f"{largura}x{altura}")

        self._centralizar(pai)

        # `focus_set` so agenda o foco; se o SO ainda tiver o foco preso
        # em outro widget (por exemplo, o console apos um modal anterior
        # fechar), o pedido fica sem efeito e o Escape/Enter param de
        # funcionar - reproduzido ao abrir este modal duas vezes seguidas.
        # `focus_force` toma o foco na hora, e sem ele nem sempre "grab"
        # bastava.
        self.janela.grab_set()
        self.janela.lift()
        if self.tem_entrada:
            self.entrada.focus_force()
        else:
            self.janela.focus_force()

    def _redesenhar_moldura(self) -> None:
        """Desenha o fundo arredondado atras do conteudo do modal."""
        largura = self.tela.winfo_width()
        altura = self.tela.winfo_height()
        if largura <= 1 or altura <= 1:
            return
        self.tela.delete("moldura")
        retangulo_redondo(
            self.tela, 0, 0, largura, altura, RAIO,
            fill=SUPERFICIE, outline=BORDA_HOVER, width=1, tags="moldura",
        )
        self.tela.tag_lower("moldura")

    def _centralizar(self, pai: tk.Tk) -> None:
        # Com `overrideredirect(True)` (sem decoracao), o Windows so
        # reflete a posicao real depois de um ciclo do laco principal -
        # `update_idletasks()` nao basta. Sem o `update()`, a janela
        # nasce em 0,0 (canto superior esquerdo da tela) por uma corrida
        # e so se corrige no proximo evento, visivel como um pulo.
        self.janela.update_idletasks()
        largura = self.janela.winfo_width()
        altura = self.janela.winfo_height()
        x = pai.winfo_rootx() + (pai.winfo_width() - largura) // 2
        y = pai.winfo_rooty() + (pai.winfo_height() - altura) // 3
        self.janela.geometry(f"+{max(0, x)}+{max(0, y)}")
        self.janela.update()

    def avisar(self, texto: str) -> None:
        """Mostra um erro dentro do proprio modal, sem fechar."""
        self.aviso.config(text=texto)

    def _confirmar(self) -> None:
        self.resultado = self.entrada.get() if self.tem_entrada else "sim"
        self.janela.destroy()

    def _cancelar(self) -> None:
        self.resultado = None
        self.janela.destroy()

    def esperar(self) -> str | None:
        """Bloqueia ate o modal fechar e devolve o resultado."""
        self.janela.wait_window()
        return self.resultado


class BarraRolagem:
    """Barra de rolagem desenhada, no lugar da `tk.Scrollbar`.

    A `tk.Scrollbar` do Windows nao aceita estilo: sai sempre com aquele
    bloco cinza de widget de sistema, com setas nas pontas. Aqui a barra
    e um Canvas fino com um polegar arredondado que some quando nao ha o
    que rolar - o comportamento que a pessoa espera de um app atual.

    Liga-se ao Text pelos dois lados: o widget avisa a barra
    (`yscrollcommand`) e a barra move o widget (arrastar / clicar).
    """

    LARGURA = 6

    def __init__(self, pai: tk.Widget, alvo: tk.Text) -> None:
        self.alvo = alvo
        self.inicio = 0.0
        self.fim = 1.0
        self._arrastando = False
        self._origem = 0.0

        self.canvas = tk.Canvas(
            pai, width=self.LARGURA, bg=CONSOLE_FUNDO,
            highlightthickness=0, bd=0,
        )
        self.polegar = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=CONSOLE_BARRA, outline="",
        )

        alvo.config(yscrollcommand=self.atualizar)
        self.canvas.bind("<Configure>", lambda _e: self._desenhar())
        self.canvas.bind("<Button-1>", self._clicar)
        self.canvas.bind("<B1-Motion>", self._arrastar)
        self.canvas.bind("<ButtonRelease-1>", self._soltar)
        self.canvas.bind("<Enter>", lambda _e: self.canvas.itemconfig(
            self.polegar, fill=CONSOLE_BARRA_ATIVA))
        self.canvas.bind("<Leave>", lambda _e: self.canvas.itemconfig(
            self.polegar, fill=CONSOLE_BARRA))

        # Roda do mouse tanto sobre o texto quanto sobre a propria barra.
        for widget in (alvo, self.canvas):
            widget.bind("<MouseWheel>", self._roda)

    def atualizar(self, inicio: str, fim: str) -> None:
        """Chamado pelo Text quando a visao muda."""
        self.inicio, self.fim = float(inicio), float(fim)
        self._desenhar()

    def _desenhar(self) -> None:
        altura = self.canvas.winfo_height()
        if altura <= 1:
            return

        # Nada a rolar: a barra some em vez de mostrar um trilho vazio.
        if self.inicio <= 0.0 and self.fim >= 1.0:
            self.canvas.itemconfig(self.polegar, state="hidden")
            return

        self.canvas.itemconfig(self.polegar, state="normal")
        topo = self.inicio * altura
        base = self.fim * altura

        # Polegar minimo: com muita saida a proporcao vira um risco de
        # 2px, impossivel de pegar com o mouse. Ao crescer, ele e
        # deslocado para dentro do trilho em vez de cortado - cortar
        # devolveria justamente o tamanho que se quis evitar.
        minimo = min(24.0, altura)
        if base - topo < minimo:
            meio = (topo + base) / 2
            topo = meio - minimo / 2
            base = topo + minimo
            if topo < 0:
                topo, base = 0.0, minimo
            elif base > altura:
                base, topo = altura, altura - minimo

        self.canvas.coords(self.polegar, 0, topo, self.LARGURA, base)

    def _fracao(self, y: int) -> float:
        altura = max(1, self.canvas.winfo_height())
        return min(1.0, max(0.0, y / altura))

    def _clicar(self, evento) -> None:
        altura = max(1, self.canvas.winfo_height())
        topo, base = self.inicio * altura, self.fim * altura
        if topo <= evento.y <= base:
            # Comecou sobre o polegar: arrasta a partir daqui.
            self._arrastando = True
            self._origem = evento.y - topo
        else:
            # Clique no trilho: pula direto para aquele ponto.
            visivel = self.fim - self.inicio
            self.alvo.yview_moveto(self._fracao(evento.y) - visivel / 2)

    def _arrastar(self, evento) -> None:
        if not self._arrastando:
            return
        self.alvo.yview_moveto(self._fracao(evento.y - self._origem))

    def _soltar(self, _evento) -> None:
        self._arrastando = False

    def _roda(self, evento) -> str:
        self.alvo.yview_scroll(-1 * (evento.delta // 120), "units")
        return "break"


class CardAcao:
    """Card clicavel desenhado em Canvas.

    Existe porque `tk.Button` nao faz canto arredondado, sombra nem
    transicao - e era isso que dava o aspecto de formulario antigo. Aqui
    cada card e um Canvas proprio que redesenha as cores em hover.
    """

    ALTURA = 66

    def __init__(
        self,
        pai: tk.Widget,
        icone: str,
        titulo: str,
        descricao: str,
        callback,
        fontes: dict[str, tkfont.Font],
        primario: bool = False,
    ) -> None:
        self.callback = callback
        self.primario = primario
        self.habilitado = True
        self.fontes = fontes
        self._animacao: str | None = None
        self._fracao = 0.0

        self.canvas = tk.Canvas(
            pai,
            height=self.ALTURA,
            bg=FUNDO,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )

        self.icone = icone
        self.titulo = titulo
        self.descricao = descricao

        self.canvas.bind("<Configure>", lambda _e: self._desenhar())
        self.canvas.bind("<Enter>", lambda _e: self._animar(1.0))
        self.canvas.bind("<Leave>", lambda _e: self._animar(0.0))
        self.canvas.bind("<Button-1>", self._pressionar)
        self.canvas.bind("<ButtonRelease-1>", self._soltar)

    # -- desenho -------------------------------------------------------

    def _cores(self) -> tuple[str, str, str, str, str]:
        """(fundo, borda, cor do titulo, cor da descricao, cor do icone)."""
        if not self.habilitado:
            return (FUNDO, BORDA, TEXTO_TENUE, TEXTO_TENUE, TEXTO_TENUE)

        if self.primario:
            fundo = misturar(TEXTO, MARCA_ESCURA, self._fracao)
            return (fundo, fundo, "#ffffff", "#e8ded9", "#ffffff")

        return (
            misturar(SUPERFICIE, SUPERFICIE_HOVER, self._fracao),
            misturar(BORDA, BORDA_HOVER, self._fracao),
            TEXTO,
            TEXTO_SUAVE,
            MARCA if self._fracao > 0.5 else TEXTO_SUAVE,
        )

    def _desenhar(self) -> None:
        largura = self.canvas.winfo_width()
        if largura <= 1:
            return

        self.canvas.delete("all")
        fundo, borda, cor_titulo, cor_desc, cor_icone = self._cores()

        # Deslocamento sutil no hover: o card "sobe" 1px.
        topo = 1 - round(self._fracao)
        base = self.ALTURA - 3 - round(self._fracao)

        # "Sombra": contorno claro logo abaixo. Sem blur no Tk, entao a
        # profundidade vem de uma faixa deslocada, nao de um halo.
        if self.habilitado and not self.primario:
            retangulo_redondo(
                self.canvas, 1, topo + 3, largura - 1, base + 3, RAIO,
                fill=SOMBRA, outline="",
            )

        retangulo_redondo(
            self.canvas, 1, topo, largura - 1, base, RAIO,
            fill=fundo, outline=borda, width=1,
        )

        self.canvas.create_text(
            26, topo + 22, text=self.icone, font=self.fontes["icone"],
            fill=cor_icone, anchor="w",
        )
        self.canvas.create_text(
            58, topo + 21, text=self.titulo, font=self.fontes["card_titulo"],
            fill=cor_titulo, anchor="w",
        )
        self.canvas.create_text(
            58, topo + 41, text=self.descricao, font=self.fontes["card_desc"],
            fill=cor_desc, anchor="w",
        )

    # -- interacao -----------------------------------------------------

    def _animar(self, alvo: float) -> None:
        """Transicao de ~200 ms entre repouso e hover."""
        if not self.habilitado:
            return
        if self._animacao is not None:
            self.canvas.after_cancel(self._animacao)
            self._animacao = None

        def passo() -> None:
            delta = 0.18 if alvo > self._fracao else -0.18
            self._fracao = min(1.0, max(0.0, self._fracao + delta))
            self._desenhar()
            if abs(self._fracao - alvo) > 0.01:
                self._animacao = self.canvas.after(16, passo)
            else:
                self._animacao = None

        passo()

    def _pressionar(self, _evento) -> None:
        """Feedback discreto de clique: o card afunda por um instante."""
        if not self.habilitado:
            return
        self.canvas.move("all", 0, 1)

    def _soltar(self, evento) -> None:
        if not self.habilitado:
            return
        self._desenhar()
        # So dispara se o cursor ainda estiver sobre o card.
        if 0 <= evento.x <= self.canvas.winfo_width() and 0 <= evento.y <= self.ALTURA:
            self.callback()

    def definir_estado(self, habilitado: bool) -> None:
        if self.habilitado == habilitado:
            return
        self.habilitado = habilitado
        self.canvas.config(cursor="hand2" if habilitado else "")
        self._fracao = 0.0
        self._desenhar()

    def definir_conteudo(self, icone: str, titulo: str, descricao: str) -> None:
        self.icone, self.titulo, self.descricao = icone, titulo, descricao
        self._desenhar()

    def definir_primario(self, primario: bool) -> None:
        if self.primario != primario:
            self.primario = primario
            self._desenhar()


class LinhaStatus:
    """Uma linha do card de status: icone, nome e badge colorida."""

    def __init__(self, pai: tk.Widget, rotulo: str, fontes: dict[str, tkfont.Font]) -> None:
        self.quadro = tk.Frame(pai, bg=SUPERFICIE)
        self.quadro.pack(fill="x", padx=22, pady=1)

        self.ponto = tk.Label(
            self.quadro, text="●", font=fontes["ponto"], bg=SUPERFICIE, fg=TEXTO_TENUE
        )
        self.ponto.pack(side="left", pady=8)

        tk.Label(
            self.quadro, text=rotulo, font=fontes["status_rotulo"],
            bg=SUPERFICIE, fg=TEXTO_SUAVE,
        ).pack(side="left", padx=(10, 0))

        # A badge e um Label com fundo proprio: e o unico jeito de ter
        # "pilula" sem Canvas, e aqui o retangulo suave basta.
        self.badge = tk.Label(
            self.quadro, text="—", font=fontes["badge"],
            bg=FUNDO, fg=TEXTO_TENUE, padx=11, pady=3,
        )
        self.badge.pack(side="right")

    def atualizar(self, texto: str, cor: str, fundo: str) -> None:
        self.ponto.config(fg=cor)
        self.badge.config(text=texto, fg=cor, bg=fundo)


class Hud:
    """Janela de entrada: estado do ambiente e acoes."""

    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.porta = PORTA_PADRAO
        self.servidor: subprocess.Popen[str] | None = None

        # As acoes rodam em thread para nao congelar a janela; a saida
        # volta por esta fila, lida pelo laco do Tkinter.
        self.fila: queue.Queue[tuple[str, str]] = queue.Queue()
        self.ocupado = False
        self.cards: dict[str, CardAcao] = {}
        self.rodando = False
        self._toast: tk.Frame | None = None
        self._toast_tarefa: str | None = None

        # Console interativo: historico de comandos e o processo em curso
        # (guardado para o Ctrl+C poder encerrar).
        self.historico: list[str] = []
        self.indice_historico = 0
        self.processo_shell: subprocess.Popen[bytes] | None = None

        # Comeca em `frontend/`: e onde vive o package.json, entao
        # `npm run dev` e `npm install` funcionam sem `cd` antes.
        self.pasta_console = FRONTEND if FRONTEND.is_dir() else RAIZ

        self._preparar_fontes()
        self._montar()
        self._ajustar_altura()
        self._drenar_fila()
        self._agendar_status()
        self._surgir()

    # ------------------------------------------------------------------
    # Fontes
    # ------------------------------------------------------------------

    def _preparar_fontes(self) -> None:
        """Resolve a familia uma vez e guarda os pesos usados.

        `Inter` e a fonte da landing; quando nao esta instalada (o caso
        comum no Windows), `Segoe UI` e a substituta mais proxima.
        """
        familia = fonte_disponivel(self.raiz, FAMILIA, "Segoe UI")
        mono = fonte_disponivel(self.raiz, FAMILIA_MONO, "Consolas")

        self.fontes = {
            "marca": tkfont.Font(family=familia, size=25, weight="bold"),
            "subtitulo": tkfont.Font(family=familia, size=10),
            "secao": tkfont.Font(family=familia, size=9, weight="bold"),
            "status_rotulo": tkfont.Font(family=familia, size=10),
            "badge": tkfont.Font(family=familia, size=9, weight="bold"),
            "ponto": tkfont.Font(family=familia, size=11),
            "card_titulo": tkfont.Font(family=familia, size=11, weight="bold"),
            "card_desc": tkfont.Font(family=familia, size=9),
            "icone": tkfont.Font(
                family=fonte_disponivel(self.raiz, FAMILIA_ICONE, "Segoe UI Symbol"), size=15
            ),
            "console": tkfont.Font(family=mono, size=10),
            "console_prompt": tkfont.Font(family=mono, size=11, weight="bold"),
            "dica": tkfont.Font(family=familia, size=8),
            "modal_titulo": tkfont.Font(family=familia, size=13, weight="bold"),
            "modal_botao": tkfont.Font(family=familia, size=9, weight="bold"),
            "modal_entrada": tkfont.Font(family=mono, size=11),
            "toast": tkfont.Font(family=familia, size=10, weight="bold"),
        }

    # ------------------------------------------------------------------
    # Montagem
    # ------------------------------------------------------------------

    def _montar(self) -> None:
        self.raiz.title("Prisma")
        self.raiz.configure(bg=FUNDO)
        # Mais largo para o console caber linha de comando sem quebrar.
        # A altura e definida depois de montar tudo (`_ajustar_altura`),
        # a partir do que o conteudo realmente pede - fixar um numero
        # aqui espremia o console, a unica secao elastica.
        self.raiz.geometry("980x1020")

        # Coluna central com margens generosas. Usa `grid` em vez de
        # `pack` para o console poder ser a unica secao que cresce: com
        # `pack`, o `expand` reparte a sobra e o console acabava menor do
        # que a altura pedida.
        self.coluna = tk.Frame(self.raiz, bg=FUNDO)
        self.coluna.pack(fill="both", expand=True, padx=ESPACO)
        self.coluna.columnconfigure(0, weight=1)
        self.coluna.rowconfigure(3, weight=1)  # so a linha do console cresce

        self._montar_cabecalho()
        self._montar_status()
        self._montar_acoes()
        self._montar_console()

    def _montar_cabecalho(self) -> None:
        cabecalho = tk.Frame(self.coluna, bg=FUNDO)
        cabecalho.grid(row=0, column=0, sticky="ew", pady=(ESPACO, 0))

        linha = tk.Frame(cabecalho, bg=FUNDO)
        linha.pack(anchor="w")

        # Marca oficial (prisma-logo-minimal.svg): mesmo triangulo com
        # aresta central e "V" da base usado no favicon e na landing
        # (frontend/src/components/ui/Logo.tsx), redesenhado aqui porque
        # o Tk nao importa SVG - so sabe desenhar linha e poligono.
        marca = tk.Canvas(linha, width=42, height=42, bg=FUNDO, highlightthickness=0)
        marca.pack(side="left")
        desenhar_logo_prisma(marca, TEXTO, tamanho=42)

        tk.Label(
            linha, text="PRISMA", font=self.fontes["marca"], bg=FUNDO, fg=TEXTO,
        ).pack(side="left", padx=(14, 0))

        tk.Label(
            cabecalho,
            text="Plataforma de estudos com IA",
            font=self.fontes["subtitulo"],
            bg=FUNDO,
            fg=TEXTO_TENUE,
        ).pack(anchor="w", pady=(3, 0))

    def _secao(self, titulo: str, linha: int) -> tk.Frame:
        """Cria um bloco rotulado na coluna central.

        Devolve o Frame onde a secao se monta. O rotulo e o conteudo
        ficam juntos para que a linha do grid represente a secao inteira.
        """
        bloco = tk.Frame(self.coluna, bg=FUNDO)
        bloco.grid(row=linha, column=0, sticky="nsew", pady=(ESPACO, 0))
        bloco.columnconfigure(0, weight=1)
        bloco.rowconfigure(1, weight=1)

        tk.Label(
            bloco, text=titulo.upper(), font=self.fontes["secao"],
            bg=FUNDO, fg=TEXTO_TENUE,
        ).grid(row=0, column=0, sticky="w", pady=(0, 9))
        return bloco

    def _montar_status(self) -> None:
        bloco = self._secao("Status", 1)

        cartao = tk.Frame(
            bloco, bg=SUPERFICIE,
            highlightbackground=BORDA, highlightthickness=1,
        )
        cartao.grid(row=1, column=0, sticky="ew")

        self.linhas: dict[str, LinhaStatus] = {}
        rotulos = ("Servidor", "Dependências", "Telas da aplicação", "npm", "Porta")
        for indice, rotulo in enumerate(rotulos):
            if indice:
                # Divisoria suave, nunca linha de tabela.
                tk.Frame(cartao, bg=BORDA, height=1).pack(fill="x", padx=22)
            self.linhas[rotulo] = LinhaStatus(cartao, rotulo, self.fontes)

        tk.Frame(cartao, bg=SUPERFICIE, height=6).pack(fill="x")

    def _montar_acoes(self) -> None:
        bloco = self._secao("Ações", 2)

        grade = tk.Frame(bloco, bg=FUNDO)
        grade.grid(row=1, column=0, sticky="ew")
        grade.columnconfigure((0, 1), weight=1, uniform="cards")

        # (chave, icone, titulo, descricao, callback, primario)
        acoes = [
            ("servidor", ICONES["rodar"], "Rodar servidor", "Inicia o Vite", self.acao_servidor, True),
            ("abrir", ICONES["navegador"], "Abrir navegador", "Abre a landing page", self.acao_abrir, False),
            ("instalar", ICONES["pacote"], "Instalar dependências", "Executa npm install", self.acao_instalar, False),
            ("sincronizar", ICONES["sincronizar"], "Sincronizar", "Atualiza as telas", self.acao_sincronizar, False),
            ("build", ICONES["build"], "Build", "Compila produção", self.acao_build, False),
            ("validar", ICONES["validar"], "Validar", "Executa lint e build", self.acao_validar, False),
            ("porta", ICONES["porta"], "Porta", f"Atual: {self.porta}", self.acao_configurar, False),
            ("limpar", ICONES["limpar"], "Limpar console", "Esvazia a saída", self.acao_limpar, False),
        ]

        for indice, (chave, icone, titulo, desc, callback, primario) in enumerate(acoes):
            card = CardAcao(grade, icone, titulo, desc, callback, self.fontes, primario)
            card.canvas.grid(
                row=indice // 2,
                column=indice % 2,
                sticky="ew",
                padx=(0, 7) if indice % 2 == 0 else (7, 0),
                pady=4,
            )
            self.cards[chave] = card

    def _montar_console(self) -> None:
        bloco = tk.Frame(self.coluna, bg=FUNDO)
        bloco.grid(row=3, column=0, sticky="nsew", pady=(ESPACO, ESPACO))
        bloco.columnconfigure(0, weight=1)
        bloco.rowconfigure(1, weight=1)

        topo = tk.Frame(bloco, bg=FUNDO)
        topo.grid(row=0, column=0, sticky="ew", pady=(0, 9))
        tk.Label(
            topo, text="▍ CONSOLE", font=self.fontes["secao"], bg=FUNDO, fg=TEXTO_TENUE,
        ).pack(side="left")
        self.rotulo_pasta = tk.Label(
            topo, text="~", font=self.fontes["dica"], bg=FUNDO, fg=TEXTO_TENUE,
        )
        self.rotulo_pasta.pack(side="right")
        tk.Label(
            topo, text="Enter executa  ·  ", font=self.fontes["dica"],
            bg=FUNDO, fg=TEXTO_TENUE,
        ).pack(side="right")

        # `pack_propagate(False)` + altura minima garantem que o console
        # nunca seja espremido a zero por falta de espaco: sem isso, numa
        # tela mais baixa a grade de acoes come a area toda e sobra so o
        # rotulo "CONSOLE".
        moldura = tk.Frame(bloco, bg=CONSOLE_FUNDO, height=ALTURA_CONSOLE)
        moldura.grid(row=1, column=0, sticky="nsew")
        moldura.pack_propagate(False)

        # A entrada e empacotada ANTES da area de saida, embora apareca
        # embaixo: o `pack` serve os primeiros widgets primeiro, e quem
        # pede `expand=True` fica com o resto. Na ordem inversa a area de
        # saida engolia tudo e a linha de comando ficava com 1px.
        self._montar_entrada(moldura)

        # Area de saida + barra de rolagem desenhada.
        area = tk.Frame(moldura, bg=CONSOLE_FUNDO)
        area.pack(fill="both", expand=True, side="top")

        self.console = tk.Text(
            area,
            font=self.fontes["console"],
            bg=CONSOLE_FUNDO,
            fg=CONSOLE_TEXTO,
            insertbackground=CONSOLE_TEXTO,
            selectbackground="#33413a",
            selectforeground="#ffffff",
            relief="flat",
            wrap="word",
            padx=18,
            pady=14,
            bd=0,
            highlightthickness=0,
        )
        self.console.pack(side="left", fill="both", expand=True)

        self.rolagem = BarraRolagem(area, self.console)
        self.rolagem.canvas.pack(side="right", fill="y", padx=(0, 7), pady=10)

        self.console.tag_config("ok", foreground=CONSOLE_OK)
        self.console.tag_config("erro", foreground=CONSOLE_ERRO)
        self.console.tag_config("suave", foreground=CONSOLE_SUAVE)
        self.console.tag_config("comando", foreground=CONSOLE_COMANDO)

        # Somente leitura para digitacao, mas ainda selecionavel e
        # copiavel: `state="disabled"` no Tk ja permite selecionar. O que
        # se digita vai para a linha de entrada abaixo, nao aqui.
        self.console.config(state="disabled")
        self.console.bind("<Button-1>", lambda _e: self.entrada.focus_set())

        self._atualizar_prompt()
        self._escrever("Pronto para começar. Digite 'help' para os comandos.", "suave")

    def _montar_entrada(self, pai: tk.Widget) -> None:
        """Linha de comando do console."""
        linha = tk.Frame(pai, bg=CONSOLE_ENTRADA)
        linha.pack(fill="x", side="bottom")

        tk.Label(
            linha, text="❯", font=self.fontes["console_prompt"],
            bg=CONSOLE_ENTRADA, fg=CONSOLE_OK, padx=0,
        ).pack(side="left", padx=(18, 8), pady=10)

        self.entrada = tk.Entry(
            linha,
            font=self.fontes["console"],
            bg=CONSOLE_ENTRADA,
            fg=CONSOLE_TEXTO,
            insertbackground=CONSOLE_TEXTO,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self.entrada.pack(side="left", fill="x", expand=True, padx=(0, 18), pady=10)

        self.entrada.bind("<Return>", self._enviar_comando)
        self.entrada.bind("<Up>", self._historico_anterior)
        self.entrada.bind("<Down>", self._historico_seguinte)
        self.entrada.bind("<Control-c>", self._interromper)

    def _ajustar_altura(self) -> None:
        """Dimensiona a janela pelo que o conteudo pede.

        As secoes de cima tem altura fixa; so o console estica. Se a
        janela abrir menor que a soma delas, o grid tira o que falta
        justamente do console - foi o que deixava a linha de comando
        espremida. Aqui a altura sai do `reqheight` real, limitada pela
        tela para nao abrir uma janela maior que o monitor.
        """
        self.raiz.update_idletasks()

        preciso = self.coluna.winfo_reqheight() + 2 * ESPACO
        disponivel = int(self.raiz.winfo_screenheight() * 0.9)
        altura = min(preciso, disponivel)
        largura = max(980, self.coluna.winfo_reqwidth() + 2 * ESPACO)

        self.raiz.geometry(f"{largura}x{altura}")
        # Minimo: tudo que e fixo, mais um console utilizavel.
        fixo = preciso - ALTURA_CONSOLE
        self.raiz.minsize(820, min(disponivel, fixo + 160))

    def _surgir(self) -> None:
        """Fade-in ao abrir: o Tk so permite alpha na janela inteira."""
        self.raiz.attributes("-alpha", 0.0)

        def passo(valor: float) -> None:
            self.raiz.attributes("-alpha", min(1.0, valor))
            if valor < 1.0:
                self.raiz.after(16, lambda: passo(valor + 0.12))

        passo(0.0)

    # ------------------------------------------------------------------
    # Console, toast e status
    # ------------------------------------------------------------------

    def _escrever(self, texto: str, tag: str = "") -> None:
        self.console.config(state="normal")
        self.console.insert("end", limpar_ansi(texto).rstrip() + "\n", tag)
        self.console.see("end")
        self.console.config(state="disabled")

    def _toast_mostrar(self, texto: str, sucesso: bool = True) -> None:
        """Aviso flutuante no rodape, que some sozinho."""
        if self._toast is not None:
            self._toast.destroy()
        if self._toast_tarefa is not None:
            self.raiz.after_cancel(self._toast_tarefa)

        cor = SUCESSO if sucesso else ERRO
        fundo = SUCESSO_FUNDO if sucesso else ERRO_FUNDO

        self._toast = tk.Frame(self.raiz, bg=fundo, highlightbackground=cor, highlightthickness=1)
        tk.Label(
            self._toast, text=f"{'✓' if sucesso else '✕'}  {texto}",
            font=self.fontes["toast"], bg=fundo, fg=cor, padx=18, pady=10,
        ).pack()
        self._toast.place(relx=0.5, rely=1.0, y=-26, anchor="s")

        self._toast_tarefa = self.raiz.after(3200, self._toast_esconder)

    def _toast_esconder(self) -> None:
        if self._toast is not None:
            self._toast.destroy()
            self._toast = None
        self._toast_tarefa = None

    def _agendar_status(self) -> None:
        """Mede o estado do ambiente fora da thread da interface.

        `porta_em_uso` bloqueia ate 0,25 s por familia de endereco - com a
        porta livre, as duas gastam o timeout. Rodar isso direto no laco
        do Tkinter congelaria a janela a cada ciclo.

        A thread NAO toca em widget nem chama `after`: o Tkinter so aceita
        chamada da thread principal ("main thread is not in main loop").
        O resultado volta pela mesma fila que a saida dos comandos usa.
        """

        def medir() -> None:
            self.fila.put(("status", "1" if porta_em_uso(self.porta) else ""))

        threading.Thread(target=medir, daemon=True).start()
        self.raiz.after(3000, self._agendar_status)

    def _pintar_status(self, porta_ocupada: bool) -> None:
        """Repinta o card de status. So roda na thread da interface."""
        meu = self.servidor is not None and self.servidor.poll() is None
        self.rodando = meu

        if porta_ocupada and meu:
            servidor = ("Rodando", SUCESSO, SUCESSO_FUNDO)
        elif porta_ocupada:
            # A porta responde, mas quem subiu nao foi este HUD.
            servidor = ("Externo", ALERTA, ALERTA_FUNDO)
        else:
            servidor = ("Parado", TEXTO_TENUE, FUNDO)

        deps = dependencias_instaladas()
        telas = app_sincronizada()
        tem_npm = npm() is not None

        self.linhas["Servidor"].atualizar(*servidor)
        self.linhas["Dependências"].atualizar(
            *(("Instaladas", SUCESSO, SUCESSO_FUNDO) if deps else ("Ausentes", ALERTA, ALERTA_FUNDO))
        )
        self.linhas["Telas da aplicação"].atualizar(
            *(("Sincronizadas", SUCESSO, SUCESSO_FUNDO) if telas else ("Ausentes", ALERTA, ALERTA_FUNDO))
        )
        self.linhas["npm"].atualizar(
            *(("Encontrado", SUCESSO, SUCESSO_FUNDO) if tem_npm else ("Ausente", ERRO, ERRO_FUNDO))
        )
        self.linhas["Porta"].atualizar(str(self.porta), INFO, INFO_FUNDO)

        # O card principal alterna entre subir e parar o servidor.
        if meu:
            self._card_servidor_para()
        elif not self.ocupado:
            self._card_servidor_roda()

        # "Abrir navegador" so faz sentido com algo respondendo.
        if not self.ocupado:
            self.cards["abrir"].definir_estado(porta_ocupada)

    # ------------------------------------------------------------------
    # Linha de comando do console
    # ------------------------------------------------------------------

    def _enviar_comando(self, _evento=None) -> str:
        """Executa o que foi digitado, como um terminal faria."""
        texto = self.entrada.get().strip()
        self.entrada.delete(0, "end")
        if not texto:
            return "break"

        self.historico.append(texto)
        self.indice_historico = len(self.historico)
        self._escrever(f"❯ {texto}", "comando")

        if self._comando_interno(texto):
            return "break"

        if self.ocupado:
            self._escrever("Já há uma ação em andamento. Ctrl+C interrompe.", "suave")
            return "break"

        self._rodar_shell(texto)
        return "break"

    def _comando_interno(self, texto: str) -> bool:
        """Atalhos que o proprio HUD resolve, sem abrir subprocesso."""
        comando = texto.lower()
        if comando in ("clear", "cls", "limpar"):
            self.acao_limpar()
            return True
        if comando in ("exit", "quit", "sair"):
            self.ao_fechar()
            return True
        if comando in ("pwd", "cd"):
            self._escrever(str(self.pasta_console), "suave")
            return True
        if comando.startswith("cd "):
            # `cd` precisa ser interno: num subprocesso ele mudaria a
            # pasta do processo filho e morreria junto com ele.
            self._mudar_pasta(texto[3:].strip().strip('"'))
            return True
        if comando in ("help", "ajuda", "?"):
            self._escrever("Digite qualquer comando de terminal. Internos:", "suave")
            self._escrever("  cd <pasta>   muda de pasta      pwd   mostra a pasta", "suave")
            self._escrever("  clear        limpa o console    exit  fecha o HUD", "suave")
            self._escrever("  Ctrl+C       interrompe o comando em andamento", "suave")
            self._escrever("  ↑ ↓          percorre o histórico", "suave")
            return True
        return False

    def _mudar_pasta(self, destino: str) -> None:
        """Muda a pasta corrente do console."""
        alvo = (self.pasta_console / destino).resolve() if destino else RAIZ
        if not alvo.is_dir():
            self._escrever(f"Pasta não encontrada: {alvo}", "erro")
            return
        self.pasta_console = alvo
        self._atualizar_prompt()
        self._escrever(str(alvo), "suave")

    def _atualizar_prompt(self) -> None:
        """Mostra no rotulo do console onde os comandos vao rodar."""
        try:
            relativo = self.pasta_console.relative_to(RAIZ)
            nome = f"~/{relativo.as_posix()}" if relativo.parts else "~"
        except ValueError:
            nome = str(self.pasta_console)
        self.rotulo_pasta.config(text=nome)

    def _rodar_shell(self, comando: str) -> None:
        """Roda um comando arbitrario na pasta corrente do console.

        Vai pelo shell para que `npm run dev`, pipes e variaveis se
        comportem como a pessoa espera do terminal.
        """
        self._travar_cards(True)

        pasta = self.pasta_console

        def trabalho() -> None:
            try:
                processo = subprocess.Popen(
                    comando, cwd=pasta, shell=True, **SAIDA_BYTES
                )
            except OSError as exc:
                self.fila.put(("erro", f"Falha ao executar: {exc}"))
                self.fila.put(("fim", ""))
                return

            self.processo_shell = processo
            assert processo.stdout is not None
            for bruto in processo.stdout:
                self.fila.put(("", decodificar(bruto).rstrip()))

            codigo = processo.wait()
            self.processo_shell = None
            if codigo != 0:
                # No Windows o codigo vem sem sinal: -4058 chega como
                # 4294963238. Converter deixa a mensagem util.
                if codigo > 2**31:
                    codigo -= 2**32
                self.fila.put(("erro", f"[saiu com código {codigo}]"))
            self.fila.put(("fim", ""))

        threading.Thread(target=trabalho, daemon=True).start()

    def _interromper(self, _evento=None) -> str:
        """Ctrl+C: encerra o comando em andamento, como num terminal."""
        processo = self.processo_shell
        if processo is not None and processo.poll() is None:
            self._escrever("^C", "suave")
            threading.Thread(
                target=encerrar_arvore, args=(processo,), daemon=True
            ).start()
        return "break"

    def _historico_anterior(self, _evento=None) -> str:
        if self.historico and self.indice_historico > 0:
            self.indice_historico -= 1
            self.entrada.delete(0, "end")
            self.entrada.insert(0, self.historico[self.indice_historico])
        return "break"

    def _historico_seguinte(self, _evento=None) -> str:
        if self.indice_historico < len(self.historico) - 1:
            self.indice_historico += 1
            self.entrada.delete(0, "end")
            self.entrada.insert(0, self.historico[self.indice_historico])
        else:
            self.indice_historico = len(self.historico)
            self.entrada.delete(0, "end")
        return "break"

    def _card_servidor_para(self) -> None:
        """Poe o card principal no modo 'parar'."""
        self.cards["servidor"].definir_conteudo(
            ICONES["parar"], "Parar servidor", "Finaliza o processo"
        )

    def _card_servidor_roda(self) -> None:
        """Poe o card principal no modo 'rodar'."""
        self.cards["servidor"].definir_conteudo(
            ICONES["rodar"], "Rodar servidor", "Inicia o Vite"
        )

    def _travar_cards(self, travar: bool) -> None:
        """Desabilita as acoes durante um comando.

        'servidor' fica de fora: parar o servidor e justamente o que a
        pessoa precisa quando algo esta em andamento.
        """
        self.ocupado = travar
        for chave, card in self.cards.items():
            if chave == "servidor":
                continue
            if chave == "abrir" and not travar:
                # Quem manda no estado deste e o _pintar_status.
                continue
            card.definir_estado(not travar)

    # ------------------------------------------------------------------
    # Execucao
    # ------------------------------------------------------------------

    def _drenar_fila(self) -> None:
        """Traz para a janela o que as threads produziram."""
        try:
            while True:
                tipo, texto = self.fila.get_nowait()
                if tipo == "fim":
                    self._travar_cards(False)
                elif tipo == "status":
                    self._pintar_status(bool(texto))
                elif tipo == "toast_ok":
                    self._toast_mostrar(texto, True)
                elif tipo == "toast_erro":
                    self._toast_mostrar(texto, False)
                else:
                    self._escrever(texto, tipo)
        except queue.Empty:
            pass
        self.raiz.after(120, self._drenar_fila)

    def _rodar_comando(
        self, argumentos: list[str], titulo: str, sucesso: str, falha: str, cwd: Path
    ) -> None:
        """Roda um comando em thread, transmitindo a saida para o console."""
        if self.ocupado:
            self._escrever("Já há uma ação em andamento.", "suave")
            return

        self._travar_cards(True)
        self._escrever(f"$ {titulo}", "suave")

        def trabalho() -> None:
            try:
                processo = subprocess.Popen(argumentos, cwd=cwd, **SAIDA_SUBPROCESSO)
            except OSError as exc:
                self.fila.put(("erro", f"Falha ao executar: {exc}"))
                self.fila.put(("toast_erro", falha))
                self.fila.put(("fim", ""))
                return

            assert processo.stdout is not None
            for linha in processo.stdout:
                self.fila.put(("", linha.rstrip()))

            if processo.wait() == 0:
                self.fila.put(("ok", sucesso))
                self.fila.put(("toast_ok", sucesso))
            else:
                self.fila.put(("erro", falha))
                self.fila.put(("toast_erro", falha))
            self.fila.put(("fim", ""))

        threading.Thread(target=trabalho, daemon=True).start()

    def _npm_ou_avisa(self) -> str | None:
        executavel = npm()
        if executavel is None:
            self._escrever("npm não encontrado no PATH.", "erro")
            self._escrever("Instale o Node.js 20+ em https://nodejs.org", "suave")
            self._toast_mostrar("npm não encontrado", False)
        return executavel

    def _deps_ou_avisa(self) -> bool:
        if dependencias_instaladas():
            return True
        self._escrever("Dependências ausentes - use 'Instalar dependências'.", "erro")
        self._toast_mostrar("Instale as dependências antes", False)
        return False

    # ------------------------------------------------------------------
    # Acoes
    # ------------------------------------------------------------------

    def acao_servidor(self) -> None:
        """Card principal: sobe ou para, conforme o estado."""
        if self.servidor and self.servidor.poll() is None:
            self._parar_servidor()
        else:
            self._subir_servidor()

    def _subir_servidor(self) -> None:
        executavel = self._npm_ou_avisa()
        if executavel is None or not self._deps_ou_avisa():
            return

        if porta_em_uso(self.porta):
            self._escrever(f"A porta {self.porta} já está em uso.", "erro")
            self._escrever("Use 'Porta' para escolher outra, ou encerre o outro processo.", "suave")
            self._toast_mostrar(f"Porta {self.porta} ocupada", False)
            return

        self._escrever(f"$ npm run dev -- --port {self.porta}", "suave")

        try:
            self.servidor = subprocess.Popen(
                [executavel, "run", "dev", "--", "--port", str(self.porta)],
                cwd=FRONTEND,
                **SAIDA_SUBPROCESSO,
            )
        except OSError as exc:
            self._escrever(f"Falha ao subir o servidor: {exc}", "erro")
            self._toast_mostrar("Não foi possível subir", False)
            return

        processo = self.servidor
        self._card_servidor_para()
        self._toast_mostrar("Servidor iniciado")

        def acompanhar() -> None:
            if processo.stdout is None:
                return
            for linha in processo.stdout:
                self.fila.put(("", linha.rstrip()))
            self.fila.put(("suave", "O servidor encerrou."))

        threading.Thread(target=acompanhar, daemon=True).start()

    def _parar_servidor(self) -> None:
        processo = self.servidor
        if processo is None or processo.poll() is not None:
            self.servidor = None
            return

        self.servidor = None
        self._escrever("Encerrando o servidor...", "suave")
        self._card_servidor_roda()

        # O wait pode levar segundos; na thread da interface isso
        # congelaria a janela justamente enquanto ela diz que esta
        # encerrando.
        def encerrar() -> None:
            encerrar_arvore(processo)
            self.fila.put(("ok", "Servidor encerrado."))
            self.fila.put(("toast_ok", "Servidor encerrado"))

        threading.Thread(target=encerrar, daemon=True).start()

    def acao_abrir(self) -> None:
        endereco = f"http://localhost:{self.porta}/"
        if not porta_em_uso(self.porta):
            self._escrever(f"Nada respondendo em {endereco}", "erro")
            self._toast_mostrar("Suba o servidor antes", False)
            return
        webbrowser.open(endereco)
        self._escrever(f"Abrindo {endereco}", "suave")

    def acao_instalar(self) -> None:
        executavel = self._npm_ou_avisa()
        if executavel is None:
            return
        self._rodar_comando(
            [executavel, "install"], "npm install",
            "Dependências instaladas.", "A instalação falhou.", FRONTEND,
        )

    def acao_build(self) -> None:
        executavel = self._npm_ou_avisa()
        if executavel is None or not self._deps_ou_avisa():
            return
        self._rodar_comando(
            [executavel, "run", "build"], "npm run build",
            "Build concluído em frontend/dist.", "O build falhou.", FRONTEND,
        )

    def acao_validar(self) -> None:
        executavel = self._npm_ou_avisa()
        if executavel is None or not self._deps_ou_avisa():
            return
        self._rodar_comando(
            [executavel, "run", "lint"], "npm run lint",
            "Lint aprovado. Rode 'Build' para completar.", "O lint reprovou.", FRONTEND,
        )

    def acao_sincronizar(self) -> None:
        if not SINCRONIZAR_APP.is_file():
            self._escrever(f"Script não encontrado: {SINCRONIZAR_APP}", "erro")
            self._toast_mostrar("Script ausente", False)
            return
        self._rodar_comando(
            [sys.executable, str(SINCRONIZAR_APP)], "python scripts/sincronizar-app.py",
            "Telas sincronizadas.", "A sincronização falhou.", RAIZ,
        )

    def acao_limpar(self) -> None:
        self.console.config(state="normal")
        self.console.delete("1.0", "end")
        self.console.config(state="disabled")
        self._escrever("Console limpo.", "suave")

    def acao_configurar(self) -> None:
        modal = Modal(
            self.raiz,
            self.fontes,
            "Porta do servidor",
            "Onde o Vite vai servir a landing.",
            confirmar="Salvar",
            valor_inicial=str(self.porta),
            dica="Entre 1024 e 65535. Enter confirma, Esc cancela.",
        )
        escolha = modal.esperar()
        if escolha is None:
            return

        texto = escolha.strip()
        if not texto.isdigit() or not 1024 <= int(texto) <= 65535:
            self._escrever(f"Porta inválida: {texto or '(vazio)'}", "erro")
            self._toast_mostrar("Porta inválida", False)
            return

        self.porta = int(texto)
        self.cards["porta"].definir_conteudo(ICONES["porta"], "Porta", f"Atual: {self.porta}")
        self._escrever(f"Porta definida para {self.porta}.", "ok")
        self._toast_mostrar(f"Porta {self.porta}")

    # ------------------------------------------------------------------

    def ao_fechar(self) -> None:
        """Nao deixa o Vite orfao quando a janela fecha."""
        processo = self.servidor
        if processo and processo.poll() is None:
            modal = Modal(
                self.raiz,
                self.fontes,
                "Encerrar o servidor?",
                "O Vite ainda está rodando. Fechar o HUD encerra o "
                "servidor junto.",
                confirmar="Encerrar",
                cancelar="Manter aberto",
            )
            if modal.esperar() is None:
                # "Manter aberto" cancela o fechamento inteiro: fechar a
                # janela assim mesmo deixaria o Vite orfao segurando a
                # porta, que e justamente o que o aviso quer evitar.
                return

            # Aqui o encerramento e sincrono de proposito: a thread do
            # `_parar_servidor` e daemon e morreria junto com o processo,
            # deixando o Vite orfao.
            self.servidor = None
            encerrar_arvore(processo)
        self.raiz.destroy()


def main() -> int:
    if not FRONTEND.is_dir():
        print(f"Pasta frontend nao encontrada em {FRONTEND}")
        return 1

    try:
        raiz = tk.Tk()
    except tk.TclError as exc:
        # Sem display (SSH, container, CI). O HUD nao tem como abrir.
        print(f"Nao foi possivel abrir a janela: {exc}\n")
        print("Sem interface grafica disponivel. Use os comandos direto:\n")
        print("  cd frontend && npm install")
        print("  cd frontend && npm run dev")
        print("  cd frontend && npm run lint && npm run build\n")
        return 1

    hud = Hud(raiz)
    raiz.protocol("WM_DELETE_WINDOW", hud.ao_fechar)
    raiz.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
