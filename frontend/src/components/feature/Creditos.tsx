import { motion } from 'motion/react'
import { Secao } from '../ui/Secao'
import { AoEntrar } from '../ui/Animar'
import { Titulo3D } from '../ui/Titulo3D'
import { creditos, perfis } from '../../content/landing'
import { SUAVE } from '../ui/movimento'

/**
 * Distribuição ilustrativa do saldo entre os perfis.
 * Fonte única: alimenta tanto a barra quanto a legenda abaixo dela,
 * para as duas nunca divergirem.
 */
const distribuicao = [
  { perfilId: 'aluno', perfil: perfis[0], valor: '54.000', pct: '45%' },
  { perfilId: 'professor', perfil: perfis[1], valor: '42.000', pct: '35%' },
  { perfilId: 'diretor', perfil: perfis[2], valor: '24.000', pct: '20%' },
].map((f) => ({ ...f, cor: f.perfil.corVar }))

/** Explica o modelo de créditos e a distribuição pelo diretor. */
export function Creditos() {
  return (
    <Secao id="creditos" fundo="diretor">
      <div className="grid items-center gap-12 lg:grid-cols-2">
        <div>
          {/* Mesma régua de capítulo das demais seções */}
          <div className="flex items-center gap-4 text-texto-secundario">
            <span className="fonte-display text-sm font-bold tracking-[0.2em]">
              04
            </span>
            <span className="h-px w-12 bg-contorno-forte" />
            <span className="text-xs tracking-[0.16em] uppercase">
              {creditos.etiqueta}
            </span>
          </div>

          <h2 className="fonte-display mt-8 text-4xl leading-[1.05] text-balance sm:text-5xl">
            <Titulo3D texto={creditos.titulo} clima="diretor" />
          </h2>
          <p className="mt-6 max-w-md text-lg leading-relaxed text-texto-secundario text-pretty">
            {creditos.descricao}
          </p>

          <ul className="mt-8 space-y-4">
            {creditos.pontos.map((ponto) => (
              <li key={ponto} className="flex gap-3">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  aria-hidden="true"
                  className="mt-0.5 shrink-0 text-texto"
                >
                  <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="1.5" opacity="0.3" />
                  <path
                    d="M6 10.5l2.5 2.5L14 7.5"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <span className="text-texto-secundario">{ponto}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Ilustracao da distribuicao do saldo */}
        <AoEntrar className="rounded-lg border border-contorno bg-superficie p-7 sm:p-8">
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-texto-secundario">Saldo da instituição</span>
            <span className="text-sm text-sucesso">ativo</span>
          </div>
          <p className="fonte-display mt-2 text-4xl">
            120.000 <span className="text-lg text-texto-secundario">créditos</span>
          </p>

          {/*
            A barra preenche da esquerda para a direita ao entrar na tela,
            deixando a proporcao entre os perfis legivel no movimento.
          */}
          <motion.div
            aria-hidden="true"
            className="mt-6 flex h-2.5 overflow-hidden rounded-full bg-superficie-alt"
            initial="oculto"
            whileInView="visivel"
            viewport={{ once: true, margin: '-80px' }}
            variants={{ visivel: { transition: { staggerChildren: 0.12 } } }}
          >
            {distribuicao.map((faixa) => (
              <motion.span
                key={faixa.perfilId}
                style={{ backgroundColor: faixa.cor }}
                variants={{
                  oculto: { width: 0 },
                  visivel: { width: faixa.pct },
                }}
                transition={{ duration: 0.7, ease: SUAVE }}
              />
            ))}
          </motion.div>

          <ul className="mt-6 space-y-3">
            {distribuicao.map(({ perfil, valor, pct }) => (
              <li key={perfil.id} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2.5">
                  <span
                    aria-hidden="true"
                    className="h-2.5 w-2.5 rounded-full"
                    style={{ backgroundColor: perfil.corVar }}
                  />
                  <span className="text-texto-secundario">{perfil.nome}</span>
                </span>
                <span className="tabular-nums">
                  {valor} <span className="text-texto-secundario">({pct})</span>
                </span>
              </li>
            ))}
          </ul>

          <p className="mt-6 border-t border-borda pt-4 text-xs text-texto-secundario">
            Números ilustrativos. O saldo real vem do ledger de créditos.
          </p>
        </AoEntrar>
      </div>
    </Secao>
  )
}
