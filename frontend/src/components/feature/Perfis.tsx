import { Card } from '../ui/Card'
import { Secao, TituloSecao } from '../ui/Secao'
import { perfis } from '../../content/landing'

/** Tres caminhos de uso: aluno, professor e diretor. */
export function Perfis() {
  return (
    <Secao id="perfis">
      <TituloSecao
        etiqueta="Perfis"
        titulo="Tres perfis, um mesmo saldo"
        descricao="Cada pessoa entra na parte da plataforma que resolve o problema dela."
      />

      <div className="mt-12 grid gap-6 md:grid-cols-3">
        {perfis.map((perfil) => (
          <Card key={perfil.id} interativo>
            <span
              aria-hidden="true"
              className="block h-1 w-12 rounded-full"
              style={{ backgroundColor: perfil.corVar }}
            />
            <h3 className="mt-5 text-xl font-semibold">{perfil.nome}</h3>
            <p className="mt-1 text-sm text-texto-secundario">{perfil.foco}</p>

            <ul className="mt-6 space-y-3">
              {perfil.itens.map((item) => (
                <li key={item} className="flex gap-3 text-sm">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 20 20"
                    fill="none"
                    aria-hidden="true"
                    className="mt-0.5 shrink-0"
                    style={{ color: perfil.corVar }}
                  >
                    <path
                      d="M4 10.5l4 4 8-8.5"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <span className="text-texto-secundario">{item}</span>
                </li>
              ))}
            </ul>
          </Card>
        ))}
      </div>
    </Secao>
  )
}
