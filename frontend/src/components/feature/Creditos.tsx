import { Secao } from '../ui/Secao'
import { creditos, perfis } from '../../content/landing'

/** Explica o modelo de creditos e a distribuicao pelo diretor. */
export function Creditos() {
  return (
    <Secao id="creditos">
      <div className="grid items-center gap-12 lg:grid-cols-2">
        <div>
          <p className="mb-3 text-sm font-semibold tracking-wide text-primaria uppercase">
            {creditos.etiqueta}
          </p>
          <h2 className="text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
            {creditos.titulo}
          </h2>
          <p className="mt-4 text-lg text-texto-secundario text-pretty">
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
                  className="mt-0.5 shrink-0 text-primaria"
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
        <div className="rounded-2xl border border-borda bg-superficie p-6 sm:p-8">
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-texto-secundario">Saldo da instituicao</span>
            <span className="text-sm font-medium text-sucesso">ativo</span>
          </div>
          <p className="mt-2 text-3xl font-semibold tracking-tight">
            120.000 <span className="text-lg font-normal text-texto-secundario">creditos</span>
          </p>

          <div
            aria-hidden="true"
            className="mt-6 flex h-2.5 overflow-hidden rounded-full bg-superficie-alt"
          >
            <span style={{ width: '45%', backgroundColor: 'var(--color-aluno)' }} />
            <span style={{ width: '35%', backgroundColor: 'var(--color-professor)' }} />
            <span style={{ width: '20%', backgroundColor: 'var(--color-diretor)' }} />
          </div>

          <ul className="mt-6 space-y-3">
            {[
              { perfil: perfis[0], valor: '54.000', pct: '45%' },
              { perfil: perfis[1], valor: '42.000', pct: '35%' },
              { perfil: perfis[2], valor: '24.000', pct: '20%' },
            ].map(({ perfil, valor, pct }) => (
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
            Numeros ilustrativos. O saldo real vem do ledger de creditos.
          </p>
        </div>
      </div>
    </Secao>
  )
}
