import { useState } from 'react'
import { Secao, TituloSecao } from '../ui/Secao'
import { exemplosRefracao } from '../../content/landing'

/**
 * Demo estatico do motor: um tema entra, tres materiais saem.
 * Ilustrativo - nao chama o backend ainda. A integracao real
 * entra na Fase 1, junto com o gateway de IA.
 */
export function MotorRefracao() {
  const [ativo, setAtivo] = useState(0)
  const exemplo = exemplosRefracao[ativo]

  return (
    <Secao id="como-funciona" alternada>
      <TituloSecao
        etiqueta="Como funciona"
        titulo="Um tema entra. Materiais prontos saem."
        descricao="Escolha um exemplo para ver o que o motor produz a partir de um unico assunto."
      />

      <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {exemplosRefracao.map((item, indice) => {
          const selecionado = indice === ativo
          return (
            <button
              key={item.entrada}
              type="button"
              aria-pressed={selecionado}
              onClick={() => setAtivo(indice)}
              className={[
                'rounded-xl border p-4 text-left text-sm transition-all duration-200',
                selecionado
                  ? 'border-primaria bg-primaria-suave text-primaria-forte shadow-sm'
                  : 'border-borda bg-superficie text-texto-secundario hover:border-primaria/40 hover:text-texto',
              ].join(' ')}
            >
              {item.entrada}
            </button>
          )
        })}
      </div>

      <div className="mt-8 rounded-2xl border border-borda bg-superficie p-6 sm:p-10">
        <div className="grid items-center gap-8 lg:grid-cols-[1fr_auto_1.4fr]">
          {/* Entrada */}
          <div>
            <p className="text-xs font-semibold tracking-wide text-texto-secundario uppercase">
              Entrada
            </p>
            <p className="mt-2 text-lg font-medium">{exemplo.entrada}</p>
          </div>

          {/* Prisma */}
          <div aria-hidden="true" className="hidden justify-center lg:flex">
            <svg width="72" height="72" viewBox="0 0 72 72" fill="none">
              <path
                d="M36 14 60 58H12L36 14Z"
                stroke="var(--color-primaria)"
                strokeWidth="2"
                strokeLinejoin="round"
              />
              <path
                d="M2 40h12"
                stroke="var(--color-texto-secundario)"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <path d="M58 34h12" stroke="var(--color-aluno)" strokeWidth="2" strokeLinecap="round" />
              <path d="M60 41h10" stroke="var(--color-professor)" strokeWidth="2" strokeLinecap="round" />
              <path d="M62 48h8" stroke="var(--color-diretor)" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </div>

          {/* Saidas */}
          <div>
            <p className="text-xs font-semibold tracking-wide text-texto-secundario uppercase">
              Saidas
            </p>
            <ul className="mt-3 space-y-2">
              {exemplo.saidas.map((saida) => (
                <li
                  key={saida}
                  className="flex items-center gap-3 rounded-lg border border-borda bg-superficie-alt px-4 py-3"
                >
                  <span
                    aria-hidden="true"
                    className="h-2 w-2 shrink-0 rounded-full bg-primaria"
                  />
                  <span className="text-sm">{saida}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <p className="mt-8 border-t border-borda pt-5 text-sm text-texto-secundario">
          Todo material gerado nasce como rascunho e passa pela revisao do professor
          antes de valer nota.
        </p>
      </div>
    </Secao>
  )
}
