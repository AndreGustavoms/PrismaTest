import type { ReactNode } from 'react'

/**
 * Tons disponíveis. Note que não há tom por perfil aqui: acento de
 * perfil é responsabilidade dos componentes de perfil, não do badge
 * (ver "REGRA DE COR" em index.css).
 */
type Tom = 'neutro' | 'destaque' | 'sucesso'

interface BadgeProps {
  children: ReactNode
  tom?: Tom
  className?: string
}

const porTom: Record<Tom, string> = {
  neutro: 'bg-transparent text-texto-secundario border-borda',
  destaque: 'bg-transparent text-texto border-texto/30',
  sucesso: 'bg-transparent text-sucesso border-sucesso/40',
}

/** Etiqueta curta de status ou categoria. */
export function Badge({ children, tom = 'neutro', className = '' }: BadgeProps) {
  return (
    <span
      className={[
        'inline-flex items-center gap-1.5 rounded-full border px-4 py-1.5',
        'text-[11px] font-semibold tracking-widest uppercase',
        porTom[tom],
        className,
      ].join(' ')}
    >
      {children}
    </span>
  )
}
