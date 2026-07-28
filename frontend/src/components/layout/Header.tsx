import { useEffect, useState } from 'react'
import { Button } from '../ui/Button'
import { LogoComNome } from '../ui/Logo'
import { navegacao } from '../../content/landing'

/** Topbar responsiva com menu colapsavel em telas pequenas. */
export function Header() {
  const [aberto, setAberto] = useState(false)
  const [rolou, setRolou] = useState(false)

  useEffect(() => {
    const aoRolar = () => setRolou(window.scrollY > 8)
    aoRolar()
    window.addEventListener('scroll', aoRolar, { passive: true })
    return () => window.removeEventListener('scroll', aoRolar)
  }, [])

  return (
    <header
      className={[
        'sticky top-0 z-50 border-b transition-colors duration-300',
        rolou
          ? 'border-borda bg-fundo/85 backdrop-blur-md'
          : 'border-transparent bg-transparent',
      ].join(' ')}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <a href="#inicio" className="text-texto">
          <LogoComNome />
        </a>

        <nav aria-label="Principal" className="hidden items-center gap-8 md:flex">
          {navegacao.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-sm text-texto-secundario transition-colors hover:text-texto"
            >
              {item.rotulo}
            </a>
          ))}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          <Button variant="ghost" size="sm" href="#entrar">
            Entrar
          </Button>
          <Button size="sm" href="#comecar">
            Comecar
          </Button>
        </div>

        <button
          type="button"
          className="md:hidden"
          aria-expanded={aberto}
          aria-controls="menu-mobile"
          aria-label={aberto ? 'Fechar menu' : 'Abrir menu'}
          onClick={() => setAberto((v) => !v)}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            {aberto ? (
              <path
                d="M6 6l12 12M18 6L6 18"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            ) : (
              <path
                d="M4 7h16M4 12h16M4 17h16"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            )}
          </svg>
        </button>
      </div>

      {aberto && (
        <div
          id="menu-mobile"
          className="border-t border-borda bg-superficie px-6 py-4 md:hidden"
        >
          <nav aria-label="Principal (mobile)" className="flex flex-col gap-1">
            {navegacao.map((item) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setAberto(false)}
                className="rounded-lg px-2 py-2.5 text-texto-secundario transition-colors hover:bg-superficie-alt hover:text-texto"
              >
                {item.rotulo}
              </a>
            ))}
          </nav>
          <div className="mt-4 flex flex-col gap-2">
            <Button variant="secondary" href="#entrar">
              Entrar
            </Button>
            <Button href="#comecar">Comecar</Button>
          </div>
        </div>
      )}
    </header>
  )
}
