import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { hero } from '../../content/landing'

/** Primeira dobra: proposta de valor e acao principal. */
export function Hero() {
  return (
    <section id="inicio" className="relative overflow-hidden px-6 pt-20 pb-16 sm:pt-28">
      {/* Halo decorativo: nao compete com o conteudo */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -top-40 left-1/2 h-96 w-[42rem] -translate-x-1/2 rounded-full opacity-50 blur-3xl"
        style={{
          background:
            'radial-gradient(circle, var(--color-primaria-suave), transparent 70%)',
        }}
      />

      <div className="relative mx-auto max-w-3xl text-center animacao-entrada">
        <Badge tom="primaria">{hero.etiqueta}</Badge>

        <h1 className="mt-6 text-4xl font-semibold tracking-tight text-balance sm:text-6xl">
          {hero.titulo}
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-texto-secundario text-pretty sm:text-xl">
          {hero.subtitulo}
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button size="lg" href="#comecar">
            {hero.ctaPrimario}
          </Button>
          <Button size="lg" variant="secondary" href="#como-funciona">
            {hero.ctaSecundario}
          </Button>
        </div>

        <p className="mt-5 text-sm text-texto-secundario">{hero.apoio}</p>
      </div>
    </section>
  )
}
