import type { ButtonHTMLAttributes, ReactNode } from 'react'

type Variant = 'primary' | 'secondary' | 'ghost'
type Size = 'sm' | 'md' | 'lg'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  /** Renderiza como <a> quando informado. Util para CTA que navega. */
  href?: string
  children: ReactNode
}

const porVariante: Record<Variant, string> = {
  primary:
    'bg-primaria text-white hover:bg-primaria-forte shadow-sm hover:shadow-md',
  secondary:
    'bg-superficie text-texto border border-borda hover:border-primaria hover:text-primaria',
  ghost: 'text-texto-secundario hover:text-texto hover:bg-superficie-alt',
}

const porTamanho: Record<Size, string> = {
  sm: 'text-sm px-3 py-1.5',
  md: 'text-sm px-5 py-2.5',
  lg: 'text-base px-7 py-3.5',
}

/**
 * Botao base do design system.
 * Variantes explicitas por prop, conforme DESIGN_SYSTEM_FRONTEND.md secao 5.
 */
export function Button({
  variant = 'primary',
  size = 'md',
  href,
  children,
  className = '',
  ...props
}: ButtonProps) {
  const estilo = [
    'inline-flex items-center justify-center gap-2 rounded-lg font-medium',
    'transition-all duration-200 ease-out',
    'disabled:opacity-50 disabled:pointer-events-none',
    porVariante[variant],
    porTamanho[size],
    className,
  ].join(' ')

  if (href) {
    return (
      <a href={href} className={estilo}>
        {children}
      </a>
    )
  }

  return (
    <button className={estilo} {...props}>
      {children}
    </button>
  )
}
