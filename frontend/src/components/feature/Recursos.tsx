import { Card } from '../ui/Card'
import { Secao, TituloSecao } from '../ui/Secao'
import { recursos } from '../../content/landing'

/** Grid de capacidades da plataforma. */
export function Recursos() {
  return (
    <Secao id="recursos" alternada>
      <TituloSecao
        etiqueta="Recursos"
        titulo="O que sustenta a plataforma"
        descricao="Decisoes tecnicas que aparecem no uso diario, nao so no diagrama."
      />

      <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {recursos.map((recurso) => (
          <Card key={recurso.titulo} interativo>
            <h3 className="text-base font-semibold">{recurso.titulo}</h3>
            <p className="mt-2 text-sm leading-relaxed text-texto-secundario">
              {recurso.descricao}
            </p>
          </Card>
        ))}
      </div>
    </Secao>
  )
}
