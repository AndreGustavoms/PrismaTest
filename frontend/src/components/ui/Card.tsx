import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  /** Realce sutil no hover. Use em cards clicaveis ou de destaque. */
  interativo?: boolean
  className?: string
}

/** Superficie base para conteudo agrupado. */
export function Card({
  children,
  interativo = false,
  className = '',
}: CardProps) {
  return (
    <div
      className={[
        'rounded-xl border border-borda bg-superficie p-6',
        interativo
          ? 'transition-all duration-300 hover:border-primaria/40 hover:shadow-lg hover:-translate-y-0.5'
          : '',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  )
}
