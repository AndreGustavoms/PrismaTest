import { LogoComNome } from '../ui/Logo'
import { marca, rodape } from '../../content/landing'

/** Rodape com navegacao em colunas. */
export function Rodape() {
  const ano = new Date().getFullYear()

  return (
    <footer className="border-t border-borda bg-superficie-alt px-6 py-14">
      <div className="mx-auto max-w-6xl">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div className="lg:col-span-1">
            <LogoComNome />
            <p className="mt-3 max-w-xs text-sm text-texto-secundario">
              {marca.descricao}
            </p>
          </div>

          {rodape.colunas.map((coluna) => (
            <nav key={coluna.titulo} aria-label={coluna.titulo}>
              <h2 className="text-sm font-semibold">{coluna.titulo}</h2>
              <ul className="mt-4 space-y-2.5">
                {coluna.links.map((link) => (
                  <li key={link.rotulo}>
                    <a
                      href={link.href}
                      className="text-sm text-texto-secundario transition-colors hover:text-texto"
                    >
                      {link.rotulo}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          ))}
        </div>

        <p className="mt-12 border-t border-borda pt-6 text-sm text-texto-secundario">
          &copy; {ano} {marca.nome}. Todos os direitos reservados.
        </p>
      </div>
    </footer>
  )
}
