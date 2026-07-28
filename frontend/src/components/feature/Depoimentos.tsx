import { Card } from '../ui/Card'
import { ItemAnimado, ListaAnimada } from '../ui/Animar'
import { Secao, TituloSecao } from '../ui/Secao'
import { depoimentos } from '../../content/landing'

/**
 * Prova social.
 * Os cards estão propositalmente vazios: substitua por relatos reais
 * coletados na instituição antes de publicar. Não preencha com texto
 * fictício apresentado como depoimento verdadeiro.
 */
export function Depoimentos() {
  return (
    <Secao fundo="professor">
      <TituloSecao
        numero="05"
        etiqueta="Depoimentos"
        titulo="Quem usa, conta"
        clima="professor"
      />

      <ListaAnimada className="mt-12 grid gap-6 md:grid-cols-3">
        {depoimentos.map((item) => (
          <ItemAnimado key={item.autor}>
            <Card className="h-full border-dashed border-contorno-forte">
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
                  <span className="block text-xs text-texto-secundario">
                    {item.papel}
                  </span>
                </span>
              </div>
            </Card>
          </ItemAnimado>
        ))}
      </ListaAnimada>
    </Secao>
  )
}
