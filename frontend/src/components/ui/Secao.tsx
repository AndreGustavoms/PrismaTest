import type { ReactNode } from 'react'

interface SecaoProps {
  id?: string
  children: ReactNode
  /** Fundo alternativo para criar ritmo vertical entre secoes vizinhas. */
  alternada?: boolean
  className?: string
}

/** Container de secao com largura maxima e respiro verticais consistentes. */
export function Secao({
  id,
  children,
  alternada = false,
  className = '',
}: SecaoProps) {
  return (
    <section
      id={id}
      className={[
        'px-6 py-20 sm:py-28',
        alternada ? 'bg-superficie-alt' : '',
        className,
      ].join(' ')}
    >
      <div className="mx-auto max-w-6xl">{children}</div>
    </section>
  )
}

interface TituloSecaoProps {
  etiqueta?: string
  titulo: string
  descricao?: string
  className?: string
}

/** Cabecalho padrao de secao: etiqueta, titulo e descricao. */
export function TituloSecao({
  etiqueta,
  titulo,
  descricao,
  className = '',
}: TituloSecaoProps) {
  return (
    <div className={['mx-auto max-w-2xl text-center', className].join(' ')}>
      {etiqueta && (
        <p className="mb-3 text-sm font-semibold tracking-wide text-primaria uppercase">
          {etiqueta}
        </p>
      )}
      <h2 className="text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
        {titulo}
      </h2>
      {descricao && (
        <p className="mt-4 text-lg text-texto-secundario text-pretty">
          {descricao}
        </p>
      )}
    </div>
  )
}
