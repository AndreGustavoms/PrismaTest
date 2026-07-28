import type { ReactNode } from 'react'

type Tom = 'neutro' | 'primaria' | 'sucesso' | 'info'

interface BadgeProps {
  children: ReactNode
  tom?: Tom
  className?: string
}

const porTom: Record<Tom, string> = {
  neutro: 'bg-superficie-alt text-texto-secundario border-borda',
  primaria: 'bg-primaria-suave text-primaria-forte border-primaria/20',
  sucesso: 'bg-sucesso/10 text-sucesso border-sucesso/20',
  info: 'bg-info/10 text-info border-info/20',
}

/** Etiqueta curta de status ou categoria. */
export function Badge({ children, tom = 'neutro', className = '' }: BadgeProps) {
  return (
    <span
      className={[
        'inline-flex items-center gap-1.5 rounded-full border px-3 py-1',
        'text-xs font-medium',
        porTom[tom],
        className,
      ].join(' ')}
    >
      {children}
    </span>
  )
}
