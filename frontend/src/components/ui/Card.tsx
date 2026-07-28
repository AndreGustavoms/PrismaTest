import type { CSSProperties, ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  /** Realce sutil no hover. Use em cards clicaveis ou de destaque. */
  interativo?: boolean
  /**
   * Cor do brilho no hover, como valor CSS. O documento de identidade
   * pede glow no tom correspondente ao card (terracota, oliva ou lavanda).
   * Sem isso, o hover apenas escurece o contorno.
   */
  brilho?: string
  className?: string
}

/** Superfície base para conteúdo agrupado. */
export function Card({
  children,
  interativo = false,
  brilho,
  className = '',
}: CardProps) {
  return (
    <div
      style={brilho ? ({ '--brilho': brilho } as CSSProperties) : undefined}
      className={[
        // Contorno nítido e sem sombra difusa (doc), porém em grafite
        // suavizado - preto sólido ficou pesado demais na tela.
        'rounded-lg border border-contorno bg-superficie p-7',
        interativo ? 'transition-shadow duration-200' : '',
        interativo && brilho
          ? 'hover:shadow-[0_0_0_3px_var(--brilho)]'
          : '',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  )
}
