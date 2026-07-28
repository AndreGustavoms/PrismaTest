import { Card } from '../ui/Card'
import { Card3D } from '../ui/Card3D'
import { ItemAnimado, ListaAnimada } from '../ui/Animar'
import { Secao, TituloSecao } from '../ui/Secao'
import { destinos, escolhaPerfil } from '../../content/destinos'

/**
 * Tela de escolha de perfil.
 *
 * É o passo entre a landing e as áreas do produto. Espelha o
 * `index.html` do repositório de concepção (`Estudo-com-IA`), que faz
 * a mesma pergunta antes de abrir a tela de cada perfil.
 *
 * IMPORTANTE: isto NÃO é autenticação. Enquanto o backend não
 * existir, qualquer pessoa escolhe qualquer perfil - é um atalho de
 * navegação, não um controle de acesso. O login real entra junto com
 * o Django (pendência registrada no IA.md).
 *
 * Quando um destino ainda não está publicado, o cartão aparece
 * desabilitado em vez de levar a um link quebrado.
 */
export function EscolhaPerfil() {
  return (
    <Secao id="entrar" fundo="branco">
      <TituloSecao
        numero={escolhaPerfil.numero}
        etiqueta={escolhaPerfil.etiqueta}
        titulo={escolhaPerfil.titulo}
        descricao={escolhaPerfil.descricao}
        clima="neutro"
      />

      <ListaAnimada className="mt-16 grid gap-6 md:grid-cols-3">
        {destinos.map((destino, indice) => {
          const disponivel = destino.href !== ''

          const conteudo = (
            <Card
              interativo={disponivel}
              className="h-full overflow-hidden p-0!"
            >
              <span
                aria-hidden="true"
                className="block h-1.5 w-full"
                style={{ backgroundColor: destino.corVar }}
              />

              <div
                className="flex h-full flex-col p-7"
                style={{ backgroundColor: destino.tintVar }}
              >
                <h3 className="text-xl">{destino.nome}</h3>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-texto-secundario">
                  {destino.resumo}
                </p>

                <span className="mt-6 inline-flex items-center gap-2 text-xs font-semibold tracking-widest uppercase">
                  {disponivel ? (
                    <>
                      Entrar
                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 16 16"
                        fill="none"
                        aria-hidden="true"
                      >
                        <path
                          d="M3 8h10M9 4l4 4-4 4"
                          stroke="currentColor"
                          strokeWidth="1.8"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </>
                  ) : (
                    <span className="text-texto-secundario">
                      {escolhaPerfil.indisponivel}
                    </span>
                  )}
                </span>
              </div>
            </Card>
          )

          return (
            <ItemAnimado
              key={destino.id}
              origem={indice % 2 === 0 ? 'esquerda' : 'direita'}
            >
              <Card3D brilho={destino.corVar} className="h-full">
                {disponivel ? (
                  <a
                    href={destino.href}
                    className="block h-full"
                    aria-label={`Entrar como ${destino.nome}`}
                  >
                    {conteudo}
                  </a>
                ) : (
                  /*
                    Sem href: `aria-disabled` avisa a tecnologia
                    assistiva de que a opção existe mas não está
                    ativa - melhor do que esconder o cartão, que
                    deixaria a pessoa sem saber que o perfil existe.
                  */
                  <div aria-disabled="true" className="h-full opacity-70">
                    {conteudo}
                  </div>
                )}
              </Card3D>
            </ItemAnimado>
          )
        })}
      </ListaAnimada>
    </Secao>
  )
}
