import { Header } from './components/layout/Header'
import { Rodape } from './components/layout/Rodape'
import { Hero } from './components/feature/Hero'
import { EscolhaPerfil } from './components/feature/EscolhaPerfil'
import { MotorRefracao } from './components/feature/MotorRefracao'
import { Perfis } from './components/feature/Perfis'
import { Recursos } from './components/feature/Recursos'
import { Creditos } from './components/feature/Creditos'
import { Depoimentos } from './components/feature/Depoimentos'
import { ChamadaFinal } from './components/feature/ChamadaFinal'

/** Landing page do Prisma. */
function App() {
  return (
    <>
      <a
        href="#conteudo"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[60] focus:rounded-lg focus:bg-primaria focus:px-4 focus:py-2 focus:text-white"
      >
        Pular para o conteúdo
      </a>

      <Header />

      <main id="conteudo">
        <Hero />
        <MotorRefracao />
        <Perfis />
        <Recursos />
        <Creditos />
        <Depoimentos />
        <ChamadaFinal />

        {/*
          Escolha de perfil: destino do "Entrar" do header e do CTA
          final. Fica no fim da página, depois dos argumentos - quem
          já decidiu chega por âncora, sem precisar rolar.
        */}
        <EscolhaPerfil />
      </main>

      <Rodape />
    </>
  )
}

export default App
