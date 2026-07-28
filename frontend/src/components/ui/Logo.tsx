interface LogoProps {
  /** Tamanho do simbolo em px. */
  tamanho?: number
  className?: string
}

/**
 * Simbolo do Prisma: um feixe entra, o triangulo refrata,
 * o espectro sai nas tres cores de perfil (aluno, professor, diretor).
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
      {/* Feixe de entrada */}
      <path
        d="M2 16h7"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.55"
      />
      {/* Corpo do prisma */}
      <path
        d="M16 5.5 27 25H5L16 5.5Z"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinejoin="round"
      />
      {/* Espectro refratado */}
      <path
        d="M23 14.5h7"
        stroke="var(--color-aluno)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M25 19h6"
        stroke="var(--color-professor)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <path
        d="M27 23.5h4"
        stroke="var(--color-diretor)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  )
}

/** Logo com nome, para header e rodape. */
export function LogoComNome({ className = '' }: { className?: string }) {
  return (
    <span className={['inline-flex items-center gap-2', className].join(' ')}>
      <Logo tamanho={26} className="text-primaria" />
      <span className="text-lg font-semibold tracking-tight">Prisma</span>
    </span>
  )
}
