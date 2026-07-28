import { Button } from '../ui/Button'
import { ctaFinal } from '../../content/landing'

/** Ultima conversao antes do rodape. */
export function ChamadaFinal() {
  return (
    <section id="comecar" className="px-6 py-20 sm:py-28">
      <div className="relative mx-auto max-w-4xl overflow-hidden rounded-2xl border border-borda bg-superficie px-6 py-16 text-center sm:px-12">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -top-24 left-1/2 h-64 w-[36rem] -translate-x-1/2 rounded-full opacity-60 blur-3xl"
          style={{
            background:
              'radial-gradient(circle, var(--color-primaria-suave), transparent 70%)',
          }}
        />

        <div className="relative">
          <h2 className="text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
            {ctaFinal.titulo}
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-texto-secundario text-pretty">
            {ctaFinal.descricao}
          </p>

          <div className="mt-9 flex justify-center">
            <Button size="lg" href="#comecar">
              {ctaFinal.botao}
            </Button>
          </div>

          <p className="mt-5 text-sm text-texto-secundario">{ctaFinal.apoio}</p>
        </div>
      </div>
    </section>
  )
}
