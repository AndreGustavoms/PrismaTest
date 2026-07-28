import { Card } from '../ui/Card'
import { Secao, TituloSecao } from '../ui/Secao'
import { depoimentos } from '../../content/landing'

/**
 * Prova social.
 * Os cards estao propositalmente vazios: substitua por relatos reais
 * coletados na instituicao antes de publicar. Nao preencha com texto
 * ficticio apresentado como depoimento verdadeiro.
 */
export function Depoimentos() {
  return (
    <Secao alternada>
      <TituloSecao
        etiqueta="Depoimentos"
        titulo="Quem usa, conta"
        descricao="Espacos reservados para relatos reais da sua instituicao."
      />

      <div className="mt-12 grid gap-6 md:grid-cols-3">
        {depoimentos.map((item) => (
          <Card key={item.autor} className="border-dashed">
            <p className="text-sm leading-relaxed text-texto-secundario italic">
              {item.texto}
            </p>
            <div className="mt-6 flex items-center gap-3 border-t border-borda pt-4">
              <span
                aria-hidden="true"
                className="flex h-9 w-9 items-center justify-center rounded-full bg-superficie-alt text-xs text-texto-secundario"
              >
                ?
              </span>
              <span className="text-sm">
                <span className="block font-medium">{item.autor}</span>
                <span className="block text-xs text-texto-secundario">{item.papel}</span>
              </span>
            </div>
          </Card>
        ))}
      </div>
    </Secao>
  )
}
