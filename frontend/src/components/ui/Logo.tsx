interface LogoProps {
  /** Tamanho do simbolo em px. */
  tamanho?: number
  className?: string
}

/**
 * Simbolo do Prisma: um feixe entra, o triangulo refrata,
 * o espectro sai nas três cores de perfil (aluno, professor, diretor).
 */
export function Logo({ tamanho = 28, className = '' }: LogoProps) {
  return (
    <svg
      width={tamanho}
      height={tamanho}
      viewBox="0 0 32 32"
      fill="none"
      role="img"
      aria-label="Prisma"
      className={className}
    >
      {/* Triangulo do prisma, traco limpo */}
      <path
        d="M16 6 28 26H4L16 6Z"
        stroke="currentColor"
        strokeWidth="2.2"
        strokeLinejoin="round"
      />
    </svg>
  )
}

/** Logo com nome, para header e rodapé. */
export function LogoComNome({ className = '' }: { className?: string }) {
  return (
    <span className={['inline-flex items-center gap-2', className].join(' ')}>
      <Logo tamanho={20} className="text-marca" />
      <span className="fonte-display text-lg font-bold tracking-[0.16em] uppercase">
        Prisma
      </span>
    </span>
  )
}
